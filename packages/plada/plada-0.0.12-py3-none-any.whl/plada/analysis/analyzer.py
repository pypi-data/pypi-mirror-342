import json
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np


class TransactionAnalyzer:
    @staticmethod
    def get_purchase_distr(result_file_path: str) -> tuple[list, list]:
        """
        シミュレーションの結果をプロットする
        
        Args:
            result_file_path (str): シミュレーションの結果のファイルパス
            
        Returns:
            tuple[list, list]: x軸: purchased count, y軸: average frequency
        """
        
        with open(result_file_path, "r") as f:
            results = json.load(f)
        
        # シミュレーションの回数を取得
        num_simulations = len(results)
        
        # 各シミュレーションでの購入回数の集計
        purchase_counts = defaultdict(float)
        
        for simulation in results:
            # 各シミュレーションの最後のステップのデータを取得
            final_step = simulation["results"][-1]
            
            # 各データの購入回数をカウント
            for data_id, data in final_step["data"].items():
                purchase_counts[data["purchased_count"]] += 1
        
        # 購入回数ごとの平均値を計算
        average_counts = {
            count : num / num_simulations
            for count, num in purchase_counts.items()
        }
        
        # x軸とy軸のデータを作成
        x = sorted(average_counts.keys())
        y = [average_counts[i] for i in x]
        
        return x, y


class MarketAnalyzer:
    pass