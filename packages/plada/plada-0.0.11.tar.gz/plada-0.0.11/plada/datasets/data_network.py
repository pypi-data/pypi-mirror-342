import random
from typing import Dict, List

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.stats import lognorm
from sklearn.linear_model import LinearRegression

from plada.datasets.data_manager import DataManager


class DataNetwork:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.graph = nx.Graph()
        
        self._create_data_network()
        
    
    def _create_data_network(self):
        """
        データネットワークを作成する。
        共通する変数を持つデータ間にエッジを張り、共通変数の数で重み付けする。
        """
        
        # データIDのリストを取得
        data_ids = list(self.data_manager.datasets.keys())
        
        # 各データをノードとして追加
        for data_id in data_ids:
            data = self.data_manager.get_data(data_id)
            self.graph.add_node(data_id, data=data)
        
        # データのペアに対して共通変数を計算し、エッジを追加
        for i, data_id1 in enumerate(data_ids):
            data1 = self.data_manager.get_data(data_id1)
            var_ids1 = {var.var_id for var in data1.variables}
            
            for data_id2 in data_ids[i+1:]:
                data2 = self.data_manager.get_data(data_id2)
                var_ids2 = {var.var_id for var in data2.variables}
                
                # 共通変数の数を計算
                common_vars = var_ids1 & var_ids2
                weight = len(common_vars)
                
                # 共通変数がある場合のみエッジを追加
                if weight > 0:
                    self.graph.add_edge(data_id1, data_id2, weight=weight)
        
        
        
        
        
        
        