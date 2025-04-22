import json
import numpy as np

class Saver:
    def __init__(self, file_path="result.json") -> None:
        """
        Saver initialization.
        
        Args:
            file_path (str): File path to save the results
        
        Returns:
            None
        """
        self.file_path = file_path
        self.results = {}
    
    def save(self, iteration, step, data_info, var_info, agent_info) -> None:
        """
        Save the results.
        
        Args:
            iteration (int): Iteration number
            step (int): Step number
            data_info (dict): Data information
            var_info (dict): Variable information
            agent_info (dict): Agent information
            
        Returns:
            None
        """
        if iteration not in self.results:
            self.results[iteration] = {}
        self.results[iteration][step] = {
            "data_info": data_info,
            "var_info": var_info,
            "agent_info": self.convert_agents_to_serializable(agent_info)  # Convert agent info
        }
    
    def write_results(self) -> None:
        """"
        Write the results to a file.
        
        Args:
            None
        Returns:
            None
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.convert_to_serializable(self.results), file, indent=4)

    def convert_to_serializable(self, data):
        """
        Convert non-serializable data (like numpy ndarrays) to a serializable format.
        
        Args:
            data: Data to be converted
        
        Returns:
            Serializable data
        """
        if isinstance(data, dict):
            return {k: self.convert_to_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_to_serializable(item) for item in data]
        elif isinstance(data, np.ndarray):
            return data.tolist()  # NumPy配列をリストに変換
        else:
            return data

    def convert_agents_to_serializable(self, agent_info):
        """
        Convert agent information to a serializable format.
        
        Args:
            agent_info (list): List of agent information
        
        Returns:
            list: List of serializable agent information
        """
        serializable_agents = []
        for agent in agent_info:
            serializable_agents.append({
                "agent_id": agent["agent_id"],
                "step_purchased_data": agent["step_purchased_data"],
                "strategy": agent["strategy"],
                "strategy_weights": agent["strategy_weights"].tolist() if isinstance(agent["strategy_weights"], np.ndarray) else agent["strategy_weights"],
                "asset": agent["asset"],
                "utility": agent["utility"],
                "state": agent["state"],
            })
        return serializable_agents