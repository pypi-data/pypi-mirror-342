import random

from ...datasets.data import Data
from ...datasets.data_manager import DataManager
from ...agents.agent import Agent


class DataEvaluator:
    def __init__(self, agent: Agent, data_manager: DataManager) -> None:
        """
        データ評価器の初期化
        """
        self.agent = agent
        self.data_manager = data_manager
        
    
    def evaluate_data(self, data: Data) -> float:
        """
        データの評価を合計して返す
        """
        
        # 各要素の評価を合計して返す
        weight_randomness: float = self.agent.weight[0]
        weight_relatedness: float = self.agent.weight[1]
        weight_ranking: float = self.agent.weight[2]
        return (
            weight_randomness * self.evaluate_data_randomness(data) + 
            weight_relatedness * self.evaluate_data_relatedness(data) + 
            weight_ranking * self.evaluate_data_ranking(data)
        ) / (weight_randomness + weight_relatedness + weight_ranking)


    def evaluate_data_randomness(self, data: Data) -> float:
        """
        データをランダムに評価
        """
        
        return random.random()


    def evaluate_data_relatedness(self, data: Data) -> float:
        """
        データを関連性によって評価
        """
        
        # エージェントが保有するデータの変数の集合
        agent_vars: set[int] = set()
        if self.agent.data: # エージェントが保有するデータが存在する場合
            for data in self.agent.data:
                agent_vars |= set(var.var_id for var in data.variables)
        else: # エージェントが保有するデータが存在しない場合
            return random.random()
        
        # 評価するデータの変数の集合
        data_vars: set[int] = set(var.var_id for var in data.variables)
        
        # エージェントが保有するデータと評価するデータの変数のdice係数
        dice: float = len(agent_vars & data_vars) / len(agent_vars | data_vars)
        return dice


    def evaluate_data_ranking(self, data: Data) -> float:
        """
        データをランキングによって評価
        """
        
        # データの累積購入回数の合計を取得
        sum: int = 0
        for data in self.data_manager.datasets.values():
            sum += data.purchased_count
        
        # 評価対象のデータの占める割合を計算
        if sum > 0:
            ratio: float = data.purchased_count / sum
            return ratio
        else:
            return random.random()