
import random

import numpy as np

from typing import Dict
from typing import List

from scipy.stats import lognorm
import networkx as nx

from ..variables.variable import Variable
from .data import Data



class DataGenerator:
    def __init__(self, num_data, variable_manager, variable_network):
        self.num_data = num_data
        self.variable_manager = variable_manager
        self.variable_network = variable_network
    
    
    def assign_var_sizes_to_data(
        self, 
        mu: float = 2.0, 
        sigma: float = 0.9, 
        min_num_variables: int = 1, 
        max_num_variables: int = 100
    ) -> Dict[int, int]:
        """
        対数正規分布に従い、データの保有変数数を生成

        Args:
            num_data (int): データの数
            mu (float): 対数正規分布の平均パラメータ
            sigma (float): 対数正規分布の標準偏差パラメータ
            min_num_variables (int): 変数の最小数
            max_num_variables (int): 変数の最大数
        
        Returns:
            var_sizes_by_data (Dict[int, int]): {データID: 変数数}の辞書
        """
        
        # 対数正規分布に従い、データの保有変数数を生成
        var_sizes_by_data: List[int] = lognorm.rvs(s=sigma, scale=np.exp(mu), size=self.num_data).astype(int)
        # 最小数と最大数の範囲内に収める
        var_sizes_by_data: List[int] = np.clip(var_sizes_by_data, min_num_variables, max_num_variables)
        
        return {data_id: var_size for data_id, var_size in enumerate(var_sizes_by_data)}


    def random_walk(self, G: nx.Graph, num_walk: int) -> List[int]:
            """
            ランダムウォークを実行する。
            
            Args:
                G (nx.Graph): グラフ
                num_walk (int): ランダムウォークの回数
            
            Returns:
                visited_var_ids (List[int]): 訪問したvar_idのリスト
            """
            
            current_node_id: int = random.choice(list(G.nodes))
            visited_vars_ids: List[int] = [self.variable_manager.get_variable(current_node_id).var_id]
            
            
            for _ in range(num_walk - 1):
                # 現在のノードの隣接ノードを取得
                neighbors: List[int] = list(G.neighbors(current_node_id))  
                # 未訪問の隣接ノードを取得
                unvisited_neighbors: List[int] = [n for n in neighbors if n not in visited_vars_ids]  
                
                if not unvisited_neighbors:
                    # 未訪問の隣接ノードがない場合、ランダムに次のノードを選択
                    next_node_id: int = random.choice(list(G.nodes))
                    while next_node_id in visited_vars_ids:
                        # すでに訪問済みのノードを選ばないようにする
                        next_node_id = random.choice(list(G.nodes))  
                else:
                    # 未訪問の隣接ノードからランダムに選択
                    next_node_id: int = random.choice(unvisited_neighbors)  
                
                # 現在のノードを更新(ウォークの進行)
                current_node_id = next_node_id  
                # 訪問したノードを訪問済みリストに追加(ウォークの記録)
                visited_vars_ids.append(current_node_id)  
                
            return visited_vars_ids
    
    
    def generate_data(self, var_sizes_by_data: Dict[int, int]) -> List[Data]:
        """
        データを生成する。
        
        Args:
            var_sizes_by_data (Dict[int, int]): {データID: 変数数}の辞書
        
        Returns:
            data_instances (List[Data]): 生成されたデータのリスト
        """
        
        data_instances: List[Data] = []
        
        for data_id, var_size in var_sizes_by_data.items():
            # ランダムウォークを実行し、訪問した変数のIDを取得
            visited_vars_ids: List[int] = self.random_walk(self.variable_network.graph, var_size)
            # 訪問した変数のIDを元に、変数のインスタンスを取得
            variables: List[Variable] = [self.variable_manager.get_variable(var_id) for var_id in visited_vars_ids]
            
            # Dataインスタンスを作成
            data = Data(data_id=data_id, variables=variables, variable_manager=self.variable_manager)
            # Dataインスタンスをリストに追加
            data_instances.append(data)
            
        return data_instances