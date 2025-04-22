import os
import json
from typing import List

from ..agents.agent import Agent
from ..agents.buyer import Buyer
from ..variables.variable_manager import VariableManager
from ..datasets.data_manager import DataManager
from ..datasets.data_network import DataNetwork
from ..transaction.transaction import Transaction


class Simulator:
    def __init__(self,
                 data_manager: DataManager,
                 variable_manager: VariableManager,
                 data_network: DataNetwork,
                 buyers: List[Buyer],
                 num_turn: int
    ):
        self.data_manager: DataManager = data_manager
        self.variable_manager: VariableManager = variable_manager
        self.data_network: DataNetwork = data_network
        self.buyers: List[Buyer] = buyers
        self.current_turn: int = 0
        self.num_turn: int = num_turn
        self.result: List[dict] = []
        self.history: List[dict] = []
    
    
    def run(self) -> List[dict]:
        """
        シミュレーションを実行
        
        Returns:
            history (List[dict]): シミュレーションの履歴
        """ 
        
        for turn in range(self.num_turn):
            self.current_turn = turn
            
            # ターン開始時の処理
            self._start_turn()
        
            # 各buyerの行動を実行
            for buyer in self.buyers:
                transaction = Transaction(
                    buyer=buyer,
                    turn=turn,
                    data_manager=self.data_manager,
                    data_network=self.data_network
                )
                result = transaction.execute()
                
                self.result.append(result)
                
            # ターン終了時の処理
            self._end_turn()
            
            # ターンの状態を保存
            self._save_state()
        
        return self.history
    
    
    def _start_turn(self):
        """
        ターン開始時の処理
        """
        # データの需要をリセット
        self.data_manager.reset_demands()
    
    
    def _end_turn(self):
        """
        ターン終了時の処理
        """
        # 変数の価格を更新
        self.variable_manager.update_prices()
        # データの価格を更新
        self.data_manager.update_prices()
        # 変数の閾値を更新
        self.variable_manager.update_thresholds()
    
    
    def _save_state(self):
        state = {
            "turn": self.current_turn,
            "variables": {
                var_id: {
                    "price": float(var.price),
                    "demand": int(var.demand),
                    "threshold": int(var.threshold)
                }
                for var_id, var in self.variable_manager.variables.items()
            },
            "data": {
                data_id: {
                    "price": float(data.price),
                    "demand": int(data.demand),
                    "purchased_count": int(data.purchased_count)
                }
                for data_id, data in self.data_manager.datasets.items()
            },
            "buyers": {
                buyer.agent_id: {
                    "assets": float(buyer.asset),
                    "data": [int(data.data_id) for data in buyer.data]
                }
                for buyer in self.buyers
            }
        }
        
        self.history.append(state)