import torch
import torch.optim as optim
import torch.nn.functional as F
from .policy_network import PolicyNetwork
from .value_network import QNetwork
from .replay_buffer import ReplayBuffer
import copy

class SACAgent:
    """
    Soft Actor-Critic (SAC) 智能体。
    适用于连续或混合动作空间。
    """
    def __init__(self, state_dim, action_dim, num_node_targets, param_dim, hidden_dim=256, lr=3e-4, gamma=0.99, tau=0.005, alpha=0.2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Actor (Policy Network)
        self.policy_net = PolicyNetwork(state_dim, action_dim, num_node_targets, param_dim).to(self.device)
        self.policy_optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)

        # Critic (Q-Networks)
        self.critic1 = QNetwork(state_dim, action_dim + num_node_targets + param_dim).to(self.device)
        self.critic2 = QNetwork(state_dim, action_dim + num_node_targets + param_dim).to(self.device)
        self.critic1_target = copy.deepcopy(self.critic1)
        self.critic2_target = copy.deepcopy(self.critic2)
        self.critic1_optimizer = optim.Adam(self.critic1.parameters(), lr=lr)
        self.critic2_optimizer = optim.Adam(self.critic2.parameters(), lr=lr)

        self.gamma = gamma
        self.tau = tau
        self.alpha = alpha # 温度参数，用于权衡奖励和熵

    def select_action(self, state):
        state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        action_type, target_node, params = self.policy_net.select_action(state)
        # 将所有动作部分拼接成一个向量
        action_vector = torch.cat([
            F.one_hot(action_type, num_classes=self.policy_net.action_head.out_features),
            F.one_hot(target_node, num_classes=self.policy_net.target_node_head.out_features),
            params
        ], dim=-1)
        return action_vector.detach().cpu().numpy().flatten()

    def train(self, replay_buffer, batch_size=256):
        if len(replay_buffer) < batch_size:
            return

        state, action, reward, next_state, done = replay_buffer.sample(batch_size)

        state = torch.FloatTensor(state).to(self.device)
        action = torch.FloatTensor(action).to(self.device)
        reward = torch.FloatTensor(reward).unsqueeze(1).to(self.device)
        next_state = torch.FloatTensor(next_state).to(self.device)
        done = torch.FloatTensor(done).unsqueeze(1).to(self.device)

        # --- 更新 Critic ---
        with torch.no_grad():
            next_action_probs, next_target_probs, next_param_mean, next_param_std = self.policy_net(next_state)
            
            # 从策略中采样下一个动作
            next_action_dist = torch.distributions.Categorical(next_action_probs)
            next_action_type = next_action_dist.sample()
            next_target_dist = torch.distributions.Categorical(next_target_probs)
            next_target_node = next_target_dist.sample()
            next_param_dist = torch.distributions.Normal(next_param_mean, next_param_std)
            next_params = next_param_dist.sample()

            # 计算动作的log-prob
            log_prob = next_action_dist.log_prob(next_action_type) + \
                       next_target_dist.log_prob(next_target_node) + \
                       next_param_dist.log_prob(next_params).sum(dim=-1)
            log_prob = log_prob.unsqueeze(1)

            # 拼接完整的下一个动作向量
            next_full_action = torch.cat([
                F.one_hot(next_action_type, num_classes=self.policy_net.action_head.out_features),
                F.one_hot(next_target_node, num_classes=self.policy_net.target_node_head.out_features),
                next_params
            ], dim=-1)

            # 目标Q值
            target_q1 = self.critic1_target(next_state, next_full_action)
            target_q2 = self.critic2_target(next_state, next_full_action)
            target_q = torch.min(target_q1, target_q2) - self.alpha * log_prob
            target_q = reward + (1 - done) * self.gamma * target_q

        # 当前Q值
        current_q1 = self.critic1(state, action)
        current_q2 = self.critic2(state, action)

        critic1_loss = F.mse_loss(current_q1, target_q)
        critic2_loss = F.mse_loss(current_q2, target_q)
        
        self.critic1_optimizer.zero_grad()
        critic1_loss.backward()
        self.critic1_optimizer.step()

        self.critic2_optimizer.zero_grad()
        critic2_loss.backward()
        self.critic2_optimizer.step()

        # --- 更新 Actor ---
        action_probs, target_probs, param_mean, param_std = self.policy_net(state)
        action_dist = torch.distributions.Categorical(action_probs)
        action_type = action_dist.sample()
        target_dist = torch.distributions.Categorical(target_probs)
        target_node = target_dist.sample()
        param_dist = torch.distributions.Normal(param_mean, param_std)
        params = param_dist.sample()
        
        log_prob = action_dist.log_prob(action_type) + \
                   target_dist.log_prob(target_node) + \
                   param_dist.log_prob(params).sum(dim=-1)
        log_prob = log_prob.unsqueeze(1)

        full_action = torch.cat([
            F.one_hot(action_type, num_classes=self.policy_net.action_head.out_features),
            F.one_hot(target_node, num_classes=self.policy_net.target_node_head.out_features),
            params
        ], dim=-1)

        q1_policy = self.critic1(state, full_action)
        q2_policy = self.critic2(state, full_action)
        min_q_policy = torch.min(q1_policy, q2_policy)
        
        policy_loss = (self.alpha * log_prob - min_q_policy).mean()

        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        self.policy_optimizer.step()
        
        # --- 更新目标网络 ---
        self.update_target_networks()

    def update_target_networks(self):
        """
        软更新目标网络参数。
        """
        for target_param, param in zip(self.critic1_target.parameters(), self.critic1.parameters()):
            target_param.data.copy_(self.tau * param.data + (1.0 - self.tau) * target_param.data)
            
        for target_param, param in zip(self.critic2_target.parameters(), self.critic2.parameters()):
            target_param.data.copy_(self.tau * param.data + (1.0 - self.tau) * target_param.data)

    def save(self, filename):
        torch.save({
            'policy_net_state_dict': self.policy_net.state_dict(),
            'critic1_state_dict': self.critic1.state_dict(),
            'critic2_state_dict': self.critic2.state_dict(),
        }, filename)

    def load(self, filename):
        checkpoint = torch.load(filename, weights_only=True)
        self.policy_net.load_state_dict(checkpoint['policy_net_state_dict'])
        self.critic1.load_state_dict(checkpoint['critic1_state_dict'])
        self.critic2.load_state_dict(checkpoint['critic2_state_dict'])
        self.critic1_target = copy.deepcopy(self.critic1)
        self.critic2_target = copy.deepcopy(self.critic2) 