from typing import List

import numpy as np
from tqdm import tqdm

from ..variables.variable import Variable
from ..variables.variable_manager import VariableManager


class Data:
    def __init__(self, 
                 data_id, 
                 variables: List[Variable], 
                 variable_manager: VariableManager) -> None:
        """
        Data initialization.
        
        Args:
            data_id (int): Data ID
            variables (list): List of variable IDs
        
        Returns:
            None
        """
        self.data_id: int = data_id
        self.price: float = 0
        self.variables: List[Variable] = variables
        self.variable_manager: VariableManager = variable_manager
        self.demand: int = 0 # データの買われた回数
        self.purchased_count: int = 0
        
        self.update_price()
    
    def reset(self):
        self.demand = 0
        self.purchased_count = 0
        self.update_price()
    
    def update_demand(self) -> None:
        """
        Update the purchase count.
        
        Args:
            buyers (list): List of Buyer instances
        
        Returns:
            None
        """
        self.demand += 1
        variables = [var for var in self.variables]
        for var in variables:
            var.demand += 1
    
    
    def reset_demand(self):
        self.demand = 0
        variables = [var for var in self.variables]
        for var in variables:
            var.demand = 0
    
    
    def update_price(self) -> None:
        """
        Update one data price.
        
        Args:
            None
        
        Returns:
            None
        """
        self.price = sum(var.price for var in self.variables)
    
    
    def update_purchased_count(self):
        self.purchased_count += self.demand
    

    def __repr__(self):
        return f"""
        Data(data_id={self.data_id},
             variables={', '.join(str(var.var_id) for var in self.variables)},
             price={self.price}, 
             demand={self.demand}, 
             purchased_count={self.purchased_count})
        """
    