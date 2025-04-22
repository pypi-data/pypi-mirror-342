import random
import networkx as nx

from ...datasets.data import Data
from .base_strategy import BaseStrategy


class RelatedStrategy(BaseStrategy):
    def select_data(self, current_data: Data) -> int:
        """
        Select data based on the related strategy.
        
        Args:
            current_data (Optional[Data]): 現在保有しているデータ

        Returns:
            int: Data ID.
        """
        # 現在いるデータが存在しない場合
        if current_data is None:
            return random.choice(list(self.data_manager.datasets.keys()))
        
        # 隣接データを取得
        current_data_id: int = current_data.data_id
        neighbors_data_ids: list[int] = list(self.data_network.graph.neighbors(current_data_id))
        
        # 隣接データが存在しない場合
        if not neighbors_data_ids:
            return random.choice(list(self.data_manager.datasets.keys()))
        
        # エッジの重みを基に確率を計算
        weights: list[float] = [
            self.data_network.graph[current_data_id][neighbor_data_id].get("weight", 1)
            for neighbor_data_id in neighbors_data_ids
        ]
        
        # 重みの合計で正規化
        total_weight: float = sum(weights)
        probabilities: list[float] = [weight / total_weight for weight in weights]
        
        # 確率に基づいてデータを選択
        return random.choices(neighbors_data_ids, weights=probabilities, k=1)[0]
