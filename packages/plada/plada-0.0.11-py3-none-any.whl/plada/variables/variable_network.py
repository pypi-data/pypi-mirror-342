from typing import Dict, Tuple

import networkx as nx

from .variable_manager import VariableManager


class VariableNetwork:
    def __init__(self, variable_manager: VariableManager):
        self.variable_manager = variable_manager
        self.graph = nx.Graph()
        
        var_degrees = {
            var_id: var.degree
            for var_id, var in self.variable_manager.variables.items()
        }
        
        self._create_variable_network_from_degrees(var_degrees)
        
        
    def _create_variable_network_from_degrees(self, var_degrees: Dict[int, int]) -> None:
        """
        Configuration Modelにより、変数の共起ネットワークを作成する。
        
        Args:
            var_degrees (Dict[int, int]): 変数と次数の辞書 {var_id: degree}
        """
        
        # Configuration Modelでネットワークを生成
        deg_seq = list(var_degrees.values())
        self.graph = nx.configuration_model(deg_seq, create_using=nx.Graph())
        
        if len(var_degrees) != self.graph.number_of_nodes():
            raise ValueError("変数の数と生成されたネットワークのノード数が一致しません。")        
