from typing import List, Dict, Type, Sequence

import numpy as np

from ..datasets.data import Data
from ..datasets.data_manager import DataManager
from ..datasets.data_network import DataNetwork
from .agent import Agent
from .seller import Seller
from .strategies.base_strategy import BaseStrategy
from .strategies.random_strategy import RandomStrategy
from .strategies.related_strategy import RelatedStrategy
from .strategies.ranking_strategy import RankingStrategy


class SellerGenerator:
    def __init__(
        self,
        num_sellers: int,
        data_manager: DataManager,
    ):
        self.num_sellers = num_sellers
        self.data_manager = data_manager

    def create_sellers(self) -> List[Seller]:
        """
        Sellerインスタンスを生成する
        
        Returns:
            List[Seller]: 生成されたSellerインスタンスのリスト
        """
        sellers: List[Seller] = []
        datasets: Sequence[Data] = list(self.data_manager.datasets.values())
        
        for i in range(self.num_sellers):
            seller: Seller = Seller(agent_id=i)

            # エージェントが保有するデータの数はランダムに0~5個
            num_dataset: int = np.random.randint(0, 6)
            
            # エージェントが保有するデータはランダムに選択
            seller.data = np.random.choice(datasets, num_dataset, replace=False)
            sellers.append(seller)
            
        return sellers