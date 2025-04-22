from dataclasses import dataclass
from typing import Optional

import numpy as np

from ..agents.agent import Agent
from ..datasets.data import Data
from ..datasets.data_manager import DataManager
from ..datasets.data_network import DataNetwork


@dataclass
class Transaction:
    def __init__(self, buyer: Agent, turn: int, data_manager: DataManager, data_network: DataNetwork):
        self.buyer = buyer
        self.turn = turn
        self.data_manager = data_manager
        self.data_network = data_network
    
    
    def execute(self) -> dict:
        result = {
            "turn": self.turn,
            "buyer": self.buyer.agent_id,
            "data_id": None,
            "success": False,
        }
        
        # 買い手が行動するかを確認
        # if self.buyer.action_probability < np.random.rand():
        #     return result
        
        # 購入候補のデータを取得
        data_id: int = self.buyer.select_data(self.data_manager, self.data_network)
        data_to_buy: Data = self.data_manager.get_data(data_id)
        
        # 条件を確認してデータを購入
        success: bool = self.buyer.buy_data(data_to_buy)
        
        # データを購入した場合
        if success:
            result["success"] = True
            result["data_id"] = data_id
            # データを購入した場合、データの需要を更新
            self.data_manager.update_demands(data_id)
            self.data_manager.update_purchased_count(data_id)
        
        return result    