import networkx as nx
import pandas as pd

def get_purchase_distr(saver):
    """
    Get the distribution of the number of purchased items
    
    Args:
        saver (Saver): Saver instance
    
    Returns:
        dict: Dictionary of the number of purchased items and the number of iterations
    """
    total_num_purchased = []
    
    for iteration, result in saver.results.items():
        each_num_purchased = {}
        for step, data in result.items():
            for item in data["data_info"]:
                data_id = item["data_id"]
                num_purchased = item["num_purchased"]
                
                if data_id not in each_num_purchased:
                    each_num_purchased[data_id] = 0
                
                each_num_purchased[data_id] += num_purchased
        total_num_purchased.append(each_num_purchased)
    
    purchase_distr = {}
    
    for result in total_num_purchased:
        for value in result.values():
            if value not in purchase_distr:
                purchase_distr[value] = 0
            purchase_distr[value] += 1

    sorted_distr = dict(sorted(purchase_distr.items()))

    return sorted_distr

def network_df(G):
    """
    使用したネットワークモデルから、分析するためのDataFrameを作成する
    
    Args:
        G (networkx.Graph): Graph object
    
    Returns:
        DataFrame: 
    """

    degrees = dict(G.degree())
    centrality = nx.eigenvector_centrality(G)
    clustering_coeffs = nx.clustering(G)
    
    data = {
        "data_id": [],
        "num_vars": [],
        "degree": [],
        "centrality": [],
        "clustering_coefficient": []
    }
    
    for node in G.nodes():
        variables = [int(var) for var in G.nodes[node]['variables'].split(',')]
        # データの追加
        data["data_id"].append(node)
        data["num_vars"].append(len(variables))
        data["degree"].append(degrees[node])
        data["centrality"].append(centrality[node])
        data["clustering_coefficient"].append(clustering_coeffs[node])
    
    df = pd.DataFrame(data)
    return df

def result_df(saver):
    """
    シミュレーションの結果からDataFrameを作成する
    
    Args:
        saver (Saver): Saver instance
    
    Returns:
        DataFrame:
    """
    dfs = []
    
    for iteration_result in saver.results.values():
        data_dict = {}
        for step_result in iteration_result.values():
            for item in step_result["data_info"]:
                data_id = item["data_id"]
                if data_id not in data_dict:
                    data_dict[data_id] = {
                        "sum_purchased": 0,
                        "final_price": item["price"],
                        "parent_tag": int(item["parent_tag"]),
                        "child_tag": int(item["child_tag"])
                    }
                data_dict[data_id]["sum_purchased"] += item["num_purchased"]
                data_dict[data_id]["final_price"] = item["price"]
    
        df = pd.DataFrame.from_dict(data_dict, orient="index").reset_index()
        df.rename(columns={"index": "data_id"}, inplace=True)
        
        df = df[["data_id", "parent_tag", "child_tag", "sum_purchased", "final_price"]]
        
        dfs.append(df)
    
    result = pd.concat(dfs, ignore_index=True)
    return result