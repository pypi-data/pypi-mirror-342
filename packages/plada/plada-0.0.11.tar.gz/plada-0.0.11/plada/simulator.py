import numpy as np

from .agents.buyer import create_buyer

def run_single_step(buyers, market, isPrice, strategy_weights, buyer_type, max_num_buyers, **kwargs) -> None:
    """
    Run a single step of the simulation.
    
    Args:
        buyers (list): List of Buyer instances
        market (Market): Market instance
        isPrice (bool): Whether to use price or not
        strategy_weights (dict): Weights for strategies
        probability (float): Probability of new buyers entering
    
    Returns:
        None
    """
    # All buyers purchase data
    for buyer in buyers:
        buyer.purchase(market.G, market, isPrice)
    
    # New buyers enter the market
    add_new_buyers(buyers, market, strategy_weights, buyer_type, max_num_buyers, a=3.0, **kwargs)

def add_new_buyers(buyers, market, strategy_weights, buyer_type, max_num_buyers, a=3.0, **kwargs) -> None:
    """
    Add new buyers to the market.
    
    Args:
        buyers (list): List of Buyer instances
        market (Market): Market instance
        strategy_weights (dict): Weights for strategies
        probability (float): Probability of new buyers entering
    
    Returns:
        None
    """
    num_new_buyers = np.random.zipf(a)
    num_new_buyers = min(num_new_buyers, max_num_buyers) # limit the number of new buyers
    # create new buyers
    for _ in range(num_new_buyers):
        new_buyer = create_buyer(strategy_weights, market, buyer_type, **kwargs)
        buyers.append(new_buyer)

def end_step(buyers) -> None:
    """
    End the step for all buyers.
    
    Args:
        buyers (list): List of Buyer instances
    
    Returns:
        None
    """
    for buyer in buyers:
        buyer.end_step()

def run_sim(buyers, market, numSteps, isPrice, strategy_weights, buyer_type, max_num_buyers, **kwargs) -> dict:
    """
    Run the simulation.
    
    Args:
        buyers (list): List of Buyer instances
        market (Market): Market instance
        numSteps (int): Number of steps
        isPrice (bool): Whether to use price or not
        strategy_weights (dict): Weights for strategies
        probability (float): Probability of new buyers entering
    
    Returns:
        dict: Dictionary of the results
    """
    saver = {}
    
    for step in range(numSteps):
        # run a single step of the simulation
        run_single_step(buyers, market, isPrice, strategy_weights, buyer_type, max_num_buyers, **kwargs)
        
        # save the results for the step
        saver[f"step_{step}"] = {
            "data_info": get_data_info(market, buyers),
            "var_info": get_var_info(market),
            "agent_info": get_agent_info(buyers)
        }
        
        # update data prices
        market.update_data_prices(buyers)
        
        # end the step for all buyers
        end_step(buyers)
    
    return saver

def get_data_info(market, buyers) -> list:
    """
    Get data information.
    
    Args:
        market (Market): Market instance
        buyers (list): List of Buyer instances
    
    Returns:
        list: List of data information
    """
    data_info = []
    
    for data in market.G.nodes():
        num_purchased = sum(
            1 for buyer in buyers if data == buyer.step_purchased_data
        )
        data_info.append({
            "data_id": data,
            "price": market.datasets[data].price,
            "num_purchased": num_purchased,
            "parent_tag": str(market.datasets[data].parent_tag),
            "child_tag": str(market.datasets[data].child_tag)
        })
    
    return data_info

def get_var_info(market) -> list:
    """
    Get variable information.
    
    Args:
        market (Market): Market instance
    
    Returns:
        list: List of variable information
    """
    var_info = []
    combined_dict = {}
    
    for data in market.G.nodes():
        variables_dict = market.datasets[data].variables
        combined_dict.update(variables_dict)
    
    sorted_var_dict = {key: combined_dict[key] for key in sorted(combined_dict)}
    
    for var_id, variable in sorted_var_dict.items():
        var_info.append({
            "var_id": variable.var_id,
            "price": variable.price
        })
    return var_info

def get_agent_info(buyers) -> list:
    """
    Get agent information.
    
    Args:
        buyers (list): List of Buyer instances
    
    Returns:
        list: List of agent information
    """
    agent_info = []
    
    for i, buyer in enumerate(buyers):
        if buyer.selected_strategy is not None:
            selected_strategy_name = buyer.selected_strategy.name
        else:
            selected_strategy_name = None
        agent_info.append({
            "agent_id": i,
            "step_purchased_data": buyer.step_purchased_data,  # the data purchased in the step
            "strategy": selected_strategy_name,
            "strategy_weights": buyer.weights,
            "asset": buyer.asset,  
            "utility": buyer.utility,  
            "state": buyer.state.name,
        })
    
    return agent_info

