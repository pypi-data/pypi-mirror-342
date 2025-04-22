from .agents.buyer_generator import BuyerGenerator
from .variables.variable_manager import VariableManager
from .variables.variable_generator import VariableFrequencyGenerator
from .variables.variable_network import VariableNetwork
from .datasets.data_generator import DataGenerator
from .datasets.data_manager import DataManager
from .datasets.data_network import DataNetwork
from .simulation.simulator import Simulator
from typing import List
import json


class Main:
    def __init__(self, config: dict):
        self.config: dict = config
        self.current_number: int = 0
        self.results: List[List[dict]] = []

    def run(self):
        return self.run_simulation(self.config)

    def run_simulation(self, config):
        """
        シミュレーションを実行する関数
        
        Args:
            config (dict): シミュレーションの設定
        """
        
        for _ in range(config["num_iterations"]):
            
            # 買い手の生成
            buyer_generator = BuyerGenerator(
                num_buyers=config["num_buyers"],
                buyer_config=config["buyer_config"]
            )
            buyers = buyer_generator.create_buyers()

            # 変数の生成
            var_manager = VariableManager()
            generator = VariableFrequencyGenerator(
                num_vars=config["num_vars"], 
                target_slope=config["target_slope"]
            )
            # zipf_param, _ = generator.optimize_zipf_param(num_iterations=100)
            var_degrees = generator.generate_var_degrees(zipf_param=1.015)
            for var_id, degree in var_degrees.items():
                var_manager.add_variable(var_id, degree)
            network = VariableNetwork(var_manager)

            # データの生成
            data_generator = DataGenerator(
                num_data=config["num_data"],
                variable_manager=var_manager,
                variable_network=network
            )
            var_sizes_by_data = data_generator.assign_var_sizes_to_data()
            data_instances = data_generator.generate_data(var_sizes_by_data)
            data_manager = DataManager()
            for data in data_instances:
                data_manager.register_data(data)
            data_network = DataNetwork(data_manager)

            # シミュレーションの実行
            simulator = Simulator(
                data_manager=data_manager,
                variable_manager=var_manager,
                data_network=data_network,
                buyers=buyers,
                num_turn=config["num_turn"]
            )

            result: List[dict] = simulator.run()
            
            self.save_results(result)
            
        return self.results
    
    
    def save_results(self, simulation_result: List[dict]):
        result = {
            "current_number": self.current_number,
            "results": simulation_result
        }
        
        self.results.append(result)
        
        self.current_number += 1
        
    
    def output_results(self, output_path: str):
        with open(output_path, "w") as f:
            json.dump(self.results, f, indent=2)
        


if __name__ == "__main__":
    # シミュレーションの設定
    config = {
        "num_iterations": 10,
        "num_buyers": 10,
        "num_vars": 10000,
        "target_slope": -2.3,
        "num_data": 100,
        "num_turn": 10,
        "buyer_config": {
            "weights": [0, 1, 0]
        }
    }
    
    # シミュレーションの実行
    main = Main(config)
    results = main.run()
    main.output_results("result/results.json")