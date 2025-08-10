import torch
import torch.optim as optim
from torch.distributions import Categorical, Normal
from .policy_network import PolicyNetwork
from .value_network import ValueNetwork

class PPOAgent:
    """
    Proximal Policy Optimization (PPO) 智能体。
    """
    def __init__(self, state_dim, action_dim, num_node_targets, param_dim, lr=3e-4, gamma=0.99, K_epochs=4, eps_clip=0.2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epochs = K_epochs
        
        # PPO 使用独立的 actor 和 critic 网络
        self.policy = PolicyNetwork(state_dim, action_dim, num_node_targets, param_dim).to(self.device)
        self.critic = ValueNetwork(state_dim).to(self.device)
        
        # 使用同一个优化器或分开
        self.optimizer = optim.Adam([
            {'params': self.policy.parameters(), 'lr': lr},
            {'params': self.critic.parameters(), 'lr': lr}
        ])
        
        # 旧策略网络，用于计算比率
        self.policy_old = PolicyNetwork(state_dim, action_dim, num_node_targets, param_dim).to(self.device)
        self.policy_old.load_state_dict(self.policy.state_dict())
        
        self.MseLoss = torch.nn.MSELoss()

    def select_action(self, state):
        with torch.no_grad():
            state = torch.FloatTensor(state).to(self.device)
            action_probs, target_probs, param_mean, param_std = self.policy_old(state)
            
            action_dist = Categorical(action_probs)
            action = action_dist.sample()
            
            target_dist = Categorical(target_probs)
            target = target_dist.sample()
            
            param_dist = Normal(param_mean, param_std)
            params = param_dist.sample()
            
            action_logprob = action_dist.log_prob(action) + \
                             target_dist.log_prob(target) + \
                             param_dist.log_prob(params).sum()
                             
        return action.item(), target.item(), params.detach().cpu().numpy(), action_logprob.item()

    def update(self, memory):
        # Monte Carlo estimate of rewards:
        rewards = []
        discounted_reward = 0
        for reward, is_terminal in zip(reversed(memory.rewards), reversed(memory.is_terminals)):
            if is_terminal:
                discounted_reward = 0
            discounted_reward = reward + (self.gamma * discounted_reward)
            rewards.insert(0, discounted_reward)
            
        # Normalizing the rewards
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.device)
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-7)

        # convert list to tensor
        old_states = torch.squeeze(torch.stack(memory.states, dim=0)).detach().to(self.device)
        old_actions = torch.squeeze(torch.stack(memory.actions, dim=0)).detach().to(self.device)
        old_logprobs = torch.squeeze(torch.tensor(memory.logprobs, dtype=torch.float32)).detach().to(self.device)
        
        # Optimize policy for K epochs
        for _ in range(self.K_epochs):
            # Evaluating old actions and values
            action_probs, target_probs, param_mean, param_std = self.policy(old_states)
            
            action_dist = Categorical(action_probs)
            target_dist = Categorical(target_probs)
            param_dist = Normal(param_mean, param_std)
            
            # 动作包含多个部分，需要分别处理
            action_type, target_node, params = old_actions[:, 0], old_actions[:, 1], old_actions[:, 2:]
            
            logprobs = action_dist.log_prob(action_type) + \
                       target_dist.log_prob(target_node) + \
                       param_dist.log_prob(params).sum(dim=-1)
            
            state_values = self.critic(old_states)
            dist_entropy = action_dist.entropy() + target_dist.entropy() + param_dist.entropy().sum(dim=-1)

            # Finding the ratio (pi_theta / pi_theta__old)
            ratios = torch.exp(logprobs - old_logprobs.detach())

            # Finding Surrogate Loss
            advantages = rewards - state_values.detach()   
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip) * advantages

            # final loss of clipped objective PPO
            loss = -torch.min(surr1, surr2) + 0.5 * self.MseLoss(state_values, rewards) - 0.01 * dist_entropy
            
            # take gradient step
            self.optimizer.zero_grad()
            loss.mean().backward()
            self.optimizer.step()
            
        # Copy new weights into old policy
        self.policy_old.load_state_dict(self.policy.state_dict())
        
        # clear buffer
        memory.clear() 