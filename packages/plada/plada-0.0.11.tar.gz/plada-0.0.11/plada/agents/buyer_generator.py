from typing import List, Dict, Type

from ..datasets.data import Data
from ..datasets.data_manager import DataManager
from ..datasets.data_network import DataNetwork
from .agent import Agent
from .buyer_v2 import Buyer
from .strategies.base_strategy import BaseStrategy
from .strategies.random_strategy import RandomStrategy
from .strategies.related_strategy import RelatedStrategy
from .strategies.ranking_strategy import RankingStrategy


class BuyerGenerator:
    def __init__(
        self,
        num_buyers: int,
    ):
        self.num_buyers = num_buyers

    def create_buyers(self) -> List[Buyer]:
        """
        Buyerインスタンスを生成する
        
        Returns:
            List[Buyer]: 生成されたBuyerインスタンスのリスト
        """
        buyers: List[Buyer] = []
        
        for i in range(self.num_buyers):
            buyer = Buyer(
                agent_id=i,
            )
            buyers.append(buyer)
            
        return buyers