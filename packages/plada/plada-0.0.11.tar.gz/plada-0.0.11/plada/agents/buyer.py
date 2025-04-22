import random
import numpy as np

from enum import Enum


class BuyerState(Enum):
    ACTIVE = 1
    WAITING = 2
    EXITED = 3
    
    
class Buyer:
    def __init__(self, strategies, weights, **kwargs) -> None:
        """
        buyer initialization.
        
        Args:
            strategies (list): List of strategy instances.
            weights (list): List of weights for each strategy.
            utility_threshold (float): Utility threshold for waiting state.
            purchase_limit (int): Purchase limit.
        
        Returns:
            None
        """
        self.purchased_data = []
        self.step_purchased_data = None
        self.asset = 200
        self.strategies = strategies
        self.selected_strategy = None # selected strategy for the current step
        self.weights = weights
        self.utility = 1
        self.total_vars = set()
        self.state = BuyerState.ACTIVE 
        self.utility_threshold = kwargs.get("utility_threshold", 0)
        self.purchase_limit = kwargs.get("purchase_limit", 10)
        self.waiting_steps = 0
    
    def purchase(self, G, market, isPrice) -> int:
        """
        Purchase data.
        
        Args:
            G (nx.Graph): Data graph.
            market (Market): Market instance.
            isPrice (bool): Whether to consider price.
        
        Returns:
            node (int): Data ID.
        """
        # check state
        # 買い手の状態を確認する
        self.check_state()
        
        # if the buyer is not active, return None
        # 買い手がアクティブでない場合はNoneを返す
        if self.state in [BuyerState.EXITED, BuyerState.WAITING]:
            self.selected_strategy = None
            return None
        
        # if the buyer is active, purchase data
        # 買い手がアクティブならばデータを購入する
        # select strategy
        strategy = random.choices(self.strategies, weights=self.weights, k=1)[0]
        self.selected_strategy = strategy
        
        # データの価値を評価する
        data_values = self.evaluate_data(G, market)
        
        # select data
        node = strategy.select_data(G, self.purchased_data)
        
        # check if the buyer can afford the data 
        if isPrice and not self.can_afford(market, node):
            return None
        
        # check if the buyer has already purchased the data
        if node in self.purchased_data:
            return None
        
        # if the buyer can purchase the data, update the purchased data
        self.step_purchased_data = node
        
        # update utility
        self.update_utility(market, node)
        
        # if considering price, update asset
        if isPrice:
            self.update_asset(market, node)
        
        return node
    
    def can_afford(self, market, data_id) -> bool:
        """
        Check if the buyer can afford the data.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            bool: Whether the buyer can afford the data.
        """
        data_price = market.datasets[data_id].price
        return data_price <= self.asset
    
    def update_asset(self, market, data_id) -> None:
        """
        Update the buyer's asset.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            None
        """
        data_price = market.datasets[data_id].price
        self.asset -= data_price
    
    def update_utility(self, market, data_id) -> None:
        """
        Update the buyer's utility.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            None
        """
        current_data_vars = set(market.datasets[data_id].variables.keys())
        # 1st purchase
        if not self.purchased_data:
            self.utility = 0
        # 2nd purchase and later
        else:
            dice_coefficient = self.calc_dice_coefficient(self.total_vars, current_data_vars)
            tag_similarity = self.calc_tag_similarity(market, data_id)
            utility = dice_coefficient + tag_similarity
            self.utility += utility
        
        # update total_vars
        self.total_vars.update(current_data_vars)
    
    def calc_dice_coefficient(self, vars_set1, vars_set2) -> float:
        """
        Calculate the Dice coefficient of variables between two data.
        
        Args:
            vars_set1 (set): Set of variables of data 1.
            vars_set2 (set): Set of variables of data 2.
        
        Returns:
            float: Dice coefficient.
        """
        intersection = vars_set1 & vars_set2
        union = vars_set1 | vars_set2
        if len(union) == 0:
            return 0
        return 2 * len(intersection) / len(union)
    
    def calc_tag_similarity(self, market, data_id) -> float:
        """
        Calculate the similarity of tags between the current data and past purchased data.
        
        Args:
            market (Market): Market instance.
            data_id (int): Data ID.
        
        Returns:
            float: Tag similarity.
        """
        # 1st purchase
        if not self.purchased_data:
            return 0
        
        total_sim = 0
        total_weight = 0
        num_purchased = len(self.purchased_data)
        
        # weighting based on the purchase order (the first purchase has the highest weight)
        for i, purchased_data in enumerate(self.purchased_data):
            current_data = market.datasets[data_id]
            past_data = market.datasets[purchased_data]
            
            weight = (i + 1) / num_purchased
            
            # compare parent and child tags
            if current_data.parent_tag == past_data.parent_tag:
                if current_data.child_tag == past_data.child_tag:
                    total_sim += weight * 1
                else:
                    total_sim += weight * 0.5
            else:
                total_sim += weight * 0
            
            total_weight += weight
            
        return total_sim / total_weight
    
    def check_state(self) -> None:
        """
        Check the buyer's state and update the state.
        
        Args:
            None
        
        Returns:
            None
        """
        # if the buyer's asset is less than 10, change the state to EXITED
        if self.asset <= 10:
            self.state = BuyerState.EXITED
            return
        
        # if the buyer's utility is less than the utility threshold, change the state to WAITING
        if self.utility < self.utility_threshold:
            self.state = BuyerState.WAITING
            self.waiting_steps = 5
            return
        
        # if the buyer has already purchased the maximum number of data, change the state to EXITED
        if len(self.purchased_data) >= self.purchase_limit:
            self.state = BuyerState.EXITED
            return
        
        # if the buyer's state is WAITING, decrease the waiting steps
        if self.state == BuyerState.WAITING:
            if self.waiting_steps > 0:
                self.waiting_steps -= 1
            else:
                self.state = BuyerState.ACTIVE
    
    def end_step(self) -> None:
        """
        End the step.
        
        Args:
            None
        
        Returns:
            None
        """
        if self.step_purchased_data is not None:
            self.purchased_data.append(self.step_purchased_data) # update purchased data at the end of the step
        self.step_purchased_data = None
    
    def evaluate_data(self, G) -> dict:
        """
        データの価値を評価する
        
        Args:
            G (nx.Graph): データグラフ
            market (Market): マーケットインスタンス
        
        Returns:
            data_values (dict): データの価値
        """
        data_values = {}
        total_weight = sum(self.weights)
        
        # 重みの合計が0の場合はエラーを出力
        if total_weight == 0:
            raise ValueError("重みの合計が0です。計算できません。")
        
        # 各データの価値を計算
        for node in G.nodes():
            d_value = self.calc_d_value(node, G)
            r_value = self.calc_r_value(node, G)
            n_value = self.calc_n_value(node, G)
        
            # 価値を更新
            value = (self.weights[0] * d_value + 
                     self.weights[1] * r_value + 
                     self.weights[2] * n_value) / total_weight
            
            data_values[node] = value
        
        return data_values
    
    def calc_d_value(self, node, G) -> float:
        """
        各データのトレンドについての価値を計算する
        """
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in G.nodes())
        
        if total_purchase_count == 0:
            return 1 / len(G.nodes())
        
        else:
            return self.market.datasets[node].purchase_count / total_purchase_count
    
    def calc_r_value(self, node, G) -> float:
        """
        各データの関連性についての価値を計算する
        """
        if not self.purchased_data:
            return 0.0
        
        last_purchased_data = self.purchased_data[-1] # 最後に購入したデータ
        return self.calc_vars_similarity(G, last_purchased_data, node)
    
    def calc_vars_similarity(self, data1, data2):
        data1_vars = set(self.market.datasets[data1].variables.keys())
        data2_vars = set(self.market.datasets[data2].variables.keys())
        
        intersection = data1_vars & data2_vars
        
        union = data1_vars | data2_vars
        if not union:
            return 0.0
        similarity =  2 * len(intersection) / len(union)
        return similarity


class RandomStrategy:
    def __init__(self) -> None:
        """
        random strategy initialization.
        
        Args:
            None
        
        Returns:
            None
        """
        self.name = "random"

    def select_data(self, G, _) -> int:
        """
        Select data randomly.
        
        Args:
            G (nx.Graph): Data graph.
            
        Returns:
            node (int): Data ID.
        """
        return random.choice(list(G.nodes()))


class RelatedStrategy:
    def __init__(self, market) -> None:
        """
        related strategy initialization.
        
        Args:
            market (Market): Market instance.
        
        Returns:
            None
        """
        self.market = market
        self.name = "related"
    
    def select_data(self, G, purchased_data) -> int:
        """
        Select data based on the related strategy.
        
        Args:
            G (nx.Graph): Data graph.
            purchased_data (list): List of purchased data.
        
        Returns:
            node (int): Data ID.
        """
        # 1st purchase
        if not purchased_data:
            return random.choice(list(G.nodes()))
        
        # 2nd purchase and later
        else:
            last_purchased_data = purchased_data[-1] # the last purchased data
            neighbors = list(G.neighbors(last_purchased_data))
            # if neighbors exist
            if neighbors:
                probabilities = self.calc_probabilities(G, neighbors)
                return random.choices(neighbors, weights=[probabilities[node] for node in neighbors])[0]
            # if neighbors do not exist
            else:
                return random.choice(list(G.nodes()))
    
    def calc_probabilities(self, G, target_nodes):
        # calculate the purchase count of the target nodes
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in target_nodes)
        if total_purchase_count == 0:
            return {node: 1 / len(target_nodes) for node in target_nodes}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(target_nodes)) for node in target_nodes}
        
        # normalize the probabilities
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


class RankingStrategy:
    def __init__(self, market) -> None:
        """
        ranking strategy initialization.
        
        Args:
            market (Market): Market instance.
        
        Returns:
            None
        """
        self.market = market
        self.name = "ranking"
    
    def select_data(self, G, _) -> int:
        """
        Select data based on the ranking strategy.
        
        Args:
            G (nx.Graph): Data graph.
            
        Returns:
            node (int): Data ID.
        """
        # calculate the probabilities of each data
        probabilities = self.calc_probabilities(G)
        
        # select data based on the probabilities
        weights = [probabilities[node] for node in list(G.nodes())]
        return random.choices(list(G.nodes()), weights=weights, k=1)[0]
    
    def calc_probabilities(self, G) -> dict:
        """
        Calculate the probabilities of each data.
        
        Args:
            G (nx.Graph): Data graph.
        
        Returns:
            probabilities (dict): Probabilities of each data.
        """
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in G.nodes())
        if total_purchase_count == 0:
            return {node: 1 / len(G.nodes()) for node in G.nodes()}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(G.nodes())) for node in G.nodes()}
        
        # normalize the probabilities
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


class FixedStrategyBuyer(Buyer):
    def __init__(self, strategies, weights, **kwargs) -> None:
        """
        buyer initialization.
        
        Args:
            strategies (list): List of strategy instances.
            weights (list): List of weights for each strategy.
            utility_threshold (float): Utility threshold for waiting state.
            purchase_limit (int): Purchase limit.
        
        Returns:
            None
        """
        super().__init__(strategies, weights, **kwargs)
        self.type = "FixedStrategyBuyer"


class LearningBuyer(Buyer):
    def __init__(self, strategies, weights, **kwargs) -> None:
        super().__init__(strategies, weights, **kwargs)
        self.type = "LearningBuyer"
        self.q_values = {strategy: 1 for strategy in strategies}  # Q値の初期化
        self.epsilon = kwargs.get("epsilon", 0.1)
        self.alpha = kwargs.get("alpha", 0.5)
        self.gamma = kwargs.get("gamma", 0.9)
        self.last_strategy = None
        self.last_utility = None
        self.selected_strategy = None

    
    def select_strategy(self):
        # ソフトマックス法による戦略選択
        q_values_array = np.array(list(self.q_values.values()))
        exp_q = np.exp(q_values_array - np.max(q_values_array))  # オーバーフロー防止のために最大値を引く
        self.weights = exp_q / np.sum(exp_q)  # weightsをここで更新

        # ε-greedy法の一部
        if random.random() < self.epsilon:
            strategy = random.choice(self.strategies)
        else:
            strategy = np.random.choice(self.strategies, p=self.weights)

        self.last_strategy = strategy
        self.selected_strategy = strategy
        return strategy

    def update_q_values(self, reward):
        if self.last_strategy is None:
            return  # last_strategyがNoneの場合は何もしない

        q_old = self.q_values[self.last_strategy]
        q_new = q_old + self.alpha * (reward + self.gamma * max(self.q_values.values()) - q_old)
        self.q_values[self.last_strategy] = q_new

    def update_weights(self):
        # Q値に基づいてweightsをリストとして更新
        total_q = sum(self.q_values.values())
        if total_q > 0:
            self.weights = np.array([q / total_q for q in self.q_values.values()])  # NumPy配列として更新
        else:
            self.weights = np.array([1 / len(self.q_values)] * len(self.q_values))  # 全て均等に
    
    def purchase(self, G, market, isPrice) -> int:
        # check state
        self.check_state()
        
        if self.state in [BuyerState.EXITED, BuyerState.WAITING]:
            self.selected_strategy = None
            return None
        
        # weightsを更新
        self.update_weights()
        
        # Select strategy based on Q-values
        strategy = self.select_strategy()
        
        # Select data based on the selected strategy
        node = strategy.select_data(G, self.purchased_data)
        
        # check if the buyer can afford the data
        if isPrice and not self.can_afford(market, node):
            return None
        
        # check if the buyer has already purchased the data
        if node in self.purchased_data:
            return None
        
        # Update the purchased data
        self.step_purchased_data = node
        
        # Update utility
        prev_utility = self.utility
        self.update_utility(market, node)
        reward = self.utility - prev_utility
        
        # Update Q-values
        if self.last_strategy is not None:  # last_strategyがNoneでないことを確認
            self.update_q_values(reward)
        
        # Update asset if considering price
        if isPrice:
            self.update_asset(market, node)
        
        return node


def create_buyer(strategy_weights, market, buyer_type, **kwargs) -> Buyer:
    """
    Create a buyer instance.
    
    Args:
        strategy_weights (dict): Dictionary of strategy names and weights.
        market (Market): Market instance.
    
    Returns:
        buyer (Buyer): Buyer instance.
    """
    # create strategy instances
    random_strategy = RandomStrategy()
    related_strategy = RelatedStrategy(market)
    ranking_strategy = RankingStrategy(market)
    
    # create a dictionary of strategies
    strategies = {
        "random": random_strategy,
        "related": related_strategy,
        "ranking": ranking_strategy
    }
    
    strategy_list = []
    weight_list = []
    
    for strategy, weight in strategy_weights.items():
        strategy_list.append(strategies[strategy])
        weight_list.append(weight)
    
    if buyer_type == "FixedStrategyBuyer":
        return FixedStrategyBuyer(strategy_list, weight_list, **kwargs)
    elif buyer_type == "LearningBuyer":
        return LearningBuyer(strategy_list, **kwargs)
    else:
        raise ValueError("Invalid buyer type.")