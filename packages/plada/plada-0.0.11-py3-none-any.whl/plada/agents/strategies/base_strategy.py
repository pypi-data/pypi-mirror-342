# strategies/base_strategy.py
from abc import ABC, abstractmethod
from typing import List

from ...datasets.data import Data
from ...datasets.data_manager import DataManager
from ...datasets.data_network import DataNetwork


class BaseStrategy(ABC):
    def __init__(self, data_manager: DataManager, data_network: DataNetwork):
        self.data_manager = data_manager
        self.data_network = data_network

    @abstractmethod
    def select_data(self, current_data: List[Data]) -> int:
        pass