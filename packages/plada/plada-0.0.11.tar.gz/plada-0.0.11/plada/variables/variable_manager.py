from typing import Dict

from .variable import Variable


class VariableManager:
    def __init__(self):
        self.variables: Dict[int, Variable] = {}
    
    def reset(self):
        """
        変数の状態をリセットする。
        """
        for var in self.variables.values():
            var.reset()
    
    
    def add_variable(self, var_id: int, degree: int):
        """
        変数をVariableManagerに追加する。
        
        Args:
            var_id (int): 変数のID
        """
        # 変数が未登録の場合、Variableを追加
        if not var_id in self.variables:
            self.variables[var_id] = Variable(var_id, degree)
    
    
    def get_variable(self, var_id: int) -> Variable:
        """
        変数を取得する
        
        Args:
            var_id (int): 変数のID
        
        Returns:
            Variable: 変数
        """
        return self.variables.get(var_id)
    
    
    def reset_demands(self):
        for var in self.variables.values():
            var.reset_demand()
    
    
    def update_prices(self):
        """
        全ての変数の価格を更新する
        """
        for var in self.variables.values():
            var.update_price()
    
    
    def update_thresholds(self):
        """
        全ての変数の閾値を更新する
        """
        for var in self.variables.values():
            var.update_threshold()