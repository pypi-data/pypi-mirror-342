from typing import List

from ..agents.agent import Agent
from ..agents.buyer import Buyer
from ..datasets.data_manager import DataManager
from ..datasets.data_network import DataNetwork
from ..transaction.transaction import Transaction


class Simulator:
    def __init__(self,
                 data_manager: DataManager,
                 data_network: DataNetwork,
                 buyers: List[Buyer],
                 num_turn: int
    ):
        self.data_manager = data_manager
        self.data_network = data_network
        self.buyers = buyers
        self.current_turn = 0
        self.num_turn = num_turn
        self.result = []
    
    
    def run(self) -> List[dict]:
        """
        シミュレーションを実行
        
        Returns:
            result (List[dict]): シミュレーションの結果
        """
        for turn in range(self.num_turn):
            self.current_turn = turn
        
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
        
        return self.result
    
    
    def _end_turn(self):
        """
        ターン終了時の処理
        """
        
        # データの価格を更新
        self.data_manager.update_prices()
        # データの需要をリセット
        self.data_manager.reset_demands()