from typing import List, Set, Tuple

import numpy as np
from scipy.stats import truncnorm

from ..datasets.data import Data


class Agent:
    def __init__(self, 
                 agent_id: int,
                 trust_dist: str = "default",
                 seed: int = None):
        self.agent_id: int = agent_id
        self.trust_score: float = 0
        self.asset: int = 0
        self.utility: float = 0
        self.data: List[Data] = [] # 保有データセット
        self.transaction_history: List[Tuple[int, int, int]] = [] # 取引履歴
        self.action_probability: float = np.random.rand()
        
        if seed is not None:
            np.random.seed(seed)
        
        self.initialize_trust_score(distribution=trust_dist)
        self.initialize_asset()
    
    def initialize_trust_score(self,
                               distribution="default"):
        if distribution == "random":
            self.trust_score = np.random.rand()
        else:
            if distribution == "high":
                mean, std = 0.7, 0.15
            elif distribution == "low":
                mean, std = 0.3, 0.15
            elif distribution == "bimodal":
                # 二峰性
                if np.random.rand() < 0.5:
                    mean, std = 0.2, 0.05
                else:
                    mean, std = 0.8, 0.05
            else:
                # デフォルト
                mean, std = 0.5, 0.15
            
            # 切断正規分布のパラメータを設定
            a, b = (0 - mean)/std, (1 - mean)/std
            # 切断正規分布から値をサンプリング
            self.trust_score = truncnorm(a, b, loc=mean, scale=std).rvs()
            # サンプリングされた値が0から1の範囲内にあることを確認
            self.trust_score = np.clip(self.trust_score, 0.0, 1.0)
    
    def initialize_asset(self,
                         min: float = 500,
                         max: float = 2500,
                         mean: float = 1500,
                         std: float = 250):
        # 切断正規分布のパラメータを設定
        a, b = (min - mean)/std, (max - mean)/std
        # 切断正規分布から値をサンプリング
        self.asset = int(truncnorm(a, b, loc=mean, scale=std).rvs())
        # サンプリングされた値がminからmaxの範囲内にあることを確認
        self.asset = np.clip(self.asset, min, max)
    
    def increase_trust_score(self, amount: float = 0.05):
        self.trust_score = min(self.trust_score + amount, 1.0)
    
    def decrease_trust_score(self, amount: float = 0.05):
        self.trust_score = max(self.trust_score - amount, 0.0)
    
    def reset(self):        
        self.trust_score = 0
        self.asset = 0
        self.utility = 0
        self.data_ids: Set[int] = set() # 保有データセットのID
        self.purchased_data = []
        self.transaction_history = [] # 取引履歴
        self.action_probability = np.random.rand()
    
    def __repr__(self):
        return f"""
        Agent(agent_id={self.agent_id}, 
              trust_score={self.trust_score:.5f}, 
              asset={self.asset}, 
              dataset={', '.join(str(data.data_id) for data in self.data)}
        """