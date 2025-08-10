from setuptools import setup, find_packages

setup(
    name="ai4qkd",
    version="0.1.0",
    packages=find_packages(),
    description="An AI-assisted design system for Quantum Key Distribution (QKD) protocols.",
    author="AI4QKD Team",
    install_requires=[
        # Add your project dependencies here from requirements.txt
        # e.g., "numpy>=1.24.0",
    ],
    python_requires='>=3.8',
) 