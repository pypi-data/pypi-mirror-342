from typing import List, Sequence

import numpy as np

from ..datasets.data import Data
from ..datasets.data_manager import DataManager
from .agent import Agent

class AgentGenerator:
    def __init__(self,
                 num_agents: int,
                 trust_dist: str = "default"):
        self.num_agents: int = num_agents
        self.trust_dist: str = trust_dist
        
    
    def create_agents(
        self,
    ) -> List[Agent]:
        """
        Agentインスタンスを生成する。
        
        Returns:
            list[Agent]: 生成されたAgentインスタンスのリスト
        """
        
        agents: List[Agent] = []
        
        for i in range(self.num_agents):
            agent: Agent = Agent(agent_id=i)
        
            agents.append(agent)
            
        return agents