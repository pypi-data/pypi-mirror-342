import random

from ..datasets.data import Data
from ..datasets.data_manager import DataManager
from ..datasets.data_network import DataNetwork
from .agent import Agent

from .strategies.base_strategy import BaseStrategy
from .strategies.random_strategy import RandomStrategy
from .strategies.related_strategy import RelatedStrategy
from .strategies.ranking_strategy import RankingStrategy


class Buyer(Agent):
    def __init__(self,
                 agent_id: int,
                 weights: list[float],
                 **kwargs):
        super().__init__(agent_id, **kwargs)   
        self.weights = weights
        
        
    def buy_data(self, data: Data) -> bool:
        """
        データを購入

        Args:
            data (Data): 購入候補のデータ

        Returns:
            bool: 購入成功かどうか
        """
        
        # 予算内で購入可能か確認
        if not self._can_afford(data):
            return False
        
        # データを保有していないか確認
        if not self._needs_data(data):
            return False
        
        # 購入
        self.asset -= data.price
        self.data.append(data)
        
        return True
    
    
    def _can_afford(self, data: Data) -> bool:
        """
        予算内で購入可能か確認
        """
        
        return self.asset >= data.price
    
    
    def _needs_data(self, data: Data) -> bool:
        """
        データを保有していないか確認
        """
        
        return data not in self.data
    
    
    def select_data(self, data_manager: DataManager, data_network: DataNetwork) -> int:
        """
        購入候補となるデータを選択
        
        Returns:
            int: 選択されたデータのID
        """
        
        # 重みに基づいてデータを選択
        strategy_class = random.choices(
            [RandomStrategy, RelatedStrategy, RankingStrategy],
            weights=self.weights,
            k=1
        )[0]
        
        # 選択された戦略に基づいてデータを選択
        strategy = strategy_class(data_manager, data_network)
        
        # 現在保有しているデータを渡す
        current_data = self.data[-1] if self.data else None
        return strategy.select_data(current_data=current_data)
    
    
    def __repr__(self):
        return f"""
        Buyer(agent_id={self.agent_id}, 
              asset={self.asset}, 
              data={', '.join(str(data.data_id) for data in self.data)},
              weights={self.weights}
              )
        """