import networkx as nx
import random

from ...datasets.data import Data
from .base_strategy import BaseStrategy

class RankingStrategy(BaseStrategy):
    def select_data(self, current_data: Data) -> int:
        """
        Select data based on the ranking strategy.
            
        Returns:
            node (int): Data ID.
        """
        
        probabilities: dict[int, float] = self.calc_probabilities()
        
        # 確率に基づいてデータを選択
        weights: list[float] = [probabilities[node_id] for node_id in list(self.data_manager.datasets.keys())]
        return random.choices(list(self.data_manager.datasets.keys()), weights=weights, k=1)[0]
    
    def calc_probabilities(self) -> dict[int, float]:
        """
        Calculate the probabilities of each data.
        
        Returns:
            probabilities (dict): Probabilities of each data.
        """
        
        # 購入回数の合計を計算
        total_count: int = sum(data.purchased_count for data in self.data_manager.datasets.values())
        
        # 各データの選択確率を計算
        probabilities: dict[int, float] = {
            node_id: (data.purchased_count + 1) / (total_count + len(self.data_manager.datasets))
            for node_id, data in self.data_manager.datasets.items()
        }
        
        # 確率の合計で正規化
        total_prob: float = sum(probabilities.values())
        return {node_id: prob / total_prob for node_id, prob in probabilities.items()}