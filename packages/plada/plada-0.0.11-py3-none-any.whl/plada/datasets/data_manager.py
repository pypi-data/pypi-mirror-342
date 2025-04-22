from typing import Dict

from .data import Data


class DataManager:
    def __init__(self):
        self.datasets: Dict[int, Data] = {}
    
    
    def reset(self):
        for data in self.datasets.values():
            data.reset()
    
    
    def register_data(self, data: Data):
        self.datasets[data.data_id] = data
    
    
    def get_data(self, data_id: int) -> Data:
        return self.datasets.get(data_id)
    
    
    def reset_demands(self):
        for data in self.datasets.values():
            data.reset_demand()
    
    
    def update_purchased_count(self, data_id: int) -> None:
        """
        指定されたデータの購入回数を更新する
        
        Args:
            data_id (int): データのID
        
        Returns:
            None
        """
        self.datasets[data_id].update_purchased_count()
    
    
    def update_prices(self):
        for data in self.datasets.values():
            data.update_price()
            

    def __repr__(self):
        return f"""
        DataManager(
            datasets={self.datasets}
        )
        """