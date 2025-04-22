from sklearn.cluster import KMeans
import numpy as np


class Market:
    def __init__(self, G) -> None:
        """
        Market initialization.
        
        Args:
            G (networkx.Graph): Graph object
        
        Returns:
            None
        """
        self.G = G
        self.datasets = {}
        self.initialize_market()
    
    def initialize_market(self) -> None:
        """
        Initialize the market.
        
        Args:
            None
        
        Returns:
            None
        """
        # create Data instances for each node
        for node in self.G.nodes():
            variables = [int(var) for var in self.G.nodes[node]['variables'].split(',')]
            self.datasets[node] = Data(node, variables)
        
        # initialize data prices
        self.initialize_data_prices()
        
        # assign tags to data considering variables
        self.assign_tags()
    
    
        
    def update_data_prices(self, buyers) -> None:
        """
        Update data prices.
        
        Args:
            buyers (list): List of Buyer instances
        
        Returns:
            None
        """
        # calculate variable demand
        var_demand = self.calc_var_demand(buyers)
        
        # update variable prices based on demand
        for data_id, data in self.datasets.items():
            data.update_var_price(var_demand)
        
        # update data prices
        self.update_data_price()
    
    def update_data_purchase_count(self, buyers) -> None:
        """
        Update data purchase count.
        
        Args:
            buyers (list): List of Buyer instances
        
        Returns:
            None
        """
        for data_id, data in self.datasets.items():
            data.update_purchase_count(buyers)
    
    def calc_var_demand(self, buyers) -> dict:
        """
        Calculate variable demand.
        
        Args:
            buyers (list): List of Buyer instances
        
        Returns:
            dict: Dictionary of variable demand
        """
        var_demand = {}
        for data_id, data in self.datasets.items():
            purchase_count = sum(1 for buyer in buyers if buyer.step_purchased_data == data_id)
            for var_id, var in data.variables.items():
                if var_id not in var_demand:
                    var_demand[var_id] = 0
                var_demand[var_id] += purchase_count
        return var_demand
    
    def update_data_price(self) -> None:
        """
        Update all data prices.
        
        Args:
            None
        
        Returns:
            None
        """
        for data_id, data in self.datasets.items():
            data.update_price()

class Data:
    def __init__(self, data_id, variables) -> None:
        """
        Data initialization.
        
        Args:
            data_id (int): Data ID
            variables (list): List of variable IDs
        
        Returns:
            None
        """
        self.data_id = data_id
        self.price = 0
        self.variables = {var_id: Variable(var_id, 10) for var_id in variables}
        self.purchase_count = 0 # the number of times the data is purchased
        self.parent_tag = None
        self.child_tag = None
    
    def update_purchase_count(self, buyers) -> None:
        """
        Update the purchase count.
        
        Args:
            buyers (list): List of Buyer instances
        
        Returns:
            None
        """
        self.purchase_count = sum(
            1 for buyer in buyers if buyer.step_purchased_data == self.data_id
        )
    
    def update_var_price(self, var_demand) -> None:
        """
        Update variable prices.
        
        Args:
            var_demand (dict): Dictionary of variable demand
        
        Returns:
            None
        """
        for var_id, var in self.variables.items():
            demand = var_demand.get(var_id, 0)
            
            # update threshold
            if demand >= var.threshold:
                var.threshold += 1
            elif demand < var.threshold:
                var.threshold = max(0, var.threshold - 1)
            
            # update price based on the updated threshold
            if demand >= var.threshold:
                var.increase_price(1)
            elif demand < var.threshold:
                var.decrease_price(1)
    
    def update_price(self) -> None:
        """
        Update one data price.
        
        Args:
            None
        
        Returns:
            None
        """
        self.price = sum(var.get_price() for var in self.variables.values())
    
    def get_vars_vector(self, max_vars_len, fill_value=-1) -> np.ndarray:
        """
        Get variables vector.
        
        Args:
            max_vars_len (int): Maximum length of variables
            fill_value (int): Fill value
        
        Returns:
            np.ndarray: Variables vector
        """
        vars_vector = np.full(max_vars_len, fill_value)
        for i, var_id in enumerate(self.variables.keys()):
            vars_vector[i] = var_id
        return vars_vector
    
    def set_parent_tag(self, parent_tag) -> None:
        """
        Set parent tag.
        
        Args:
            parent_tag (int): Parent tag
        
        Returns:
            None
        """
        self.parent_tag = parent_tag
    
    def set_child_tag(self, child_tag) -> None:
        """
        Set child tag.
        
        Args:
            child_tag (int): Child tag
        
        Returns:
            None
        """
        self.child_tag = child_tag

class Variable:
    def __init__(self, var_id, price=10) -> None:
        """
        Variable initialization.
        
        Args:
            var_id (int): Variable ID
            price (int): Price
        
        Returns:
            None
        """
        self.var_id = var_id
        self.price = price
        self.threshold = 1
    
    def set_price(self, price) -> None:
        """
        Set the price.
        
        Args:
            price (int): Price
        
        Returns:
            None
        """
        self.price = price
    
    def get_price(self) -> int:
        """
        Get the price.
        
        Args:
            None
        
        Returns:
            int: Price
        """
        return self.price
    
    def increase_price(self, amount) -> None:
        """
        Increase the price.
        
        Args:
            amount (int): Amount to increase
        
        Returns:
            None
        """
        self.price += amount
    
    def decrease_price(self, amount) -> None:
        """
        Decrease the price.
        
        Args:
            amount (int): Amount to decrease
        
        Returns:
            None
        """
        self.price = max(0, self.price - amount)