import random

from .base_strategy import BaseStrategy


class RandomStrategy(BaseStrategy):
    def select_data(self) -> int:
        """
        Select data randomly.
            
        Returns:
            node (int): Data ID.
        """
        
        return random.choice(list(self.data_manager.datasets.keys()))