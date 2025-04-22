from ..datasets.data import Data
from .agent import Agent

class Seller(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def sell_data(self, data: Data) -> None:
        """
        データを売却
        """
        self.asset += data.price
        
    def __repr__(self):
        return f"""
        Seller(agent_id={self.agent_id}, 
               asset={self.asset}, 
               data={', '.join(str(data.data_id) for data in self.data)},
               )
        """