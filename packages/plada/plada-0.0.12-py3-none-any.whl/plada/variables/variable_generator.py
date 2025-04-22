from typing import Dict
from typing import Tuple

import numpy as np
from sklearn.linear_model import LinearRegression
from tqdm import tqdm


class VariableFrequencyGenerator:
    def __init__(self, num_vars: int, target_slope: float):
        self.num_vars = num_vars
        self.target_slope = target_slope
        
    
    def optimize_zipf_param(self, num_iterations: int) -> Tuple[float, float]:
        """
        目標のべき指数に最も近いZipfのパラメータを見つける。

        Args:
            num_vars (int): 変数の数
            num_iterations (int): 計算回数
        
        Returns:
            Tuple[float, float]: 最適なZipfのパラメータとその時のべき指数
        """
    
        best_zipf_param = None
        best_slope = None
        min_diff = float('inf')
            
        for zipf_param in tqdm(np.arange(1.001, 1.2, 0.001), desc="Optimizing Zipf's parameter"):
            slopes = []
            
            for _ in range(num_iterations):
                # zipf分布から変数を生成する
                zipf_vars = np.random.zipf(zipf_param, self.num_vars)
                
                # 変数の出現頻度をカウントする
                vars_, counts = np.unique(zipf_vars, return_counts=True)
                
                # 出現頻度の降順にソートする
                sort_indices = np.argsort(counts)[::-1]
                counts_sorted = counts[sort_indices]
                
                # ランクを計算する
                rank = np.arange(1, len(counts_sorted) + 1)
                log_rank = np.log10(rank)
                log_counts = np.log10(counts_sorted)
                
                # 最小二乗法でrank-frequencyの傾きを求める
                model = LinearRegression().fit(log_counts.reshape(-1, 1), log_rank)
                slope = model.coef_[0]
                slopes.append(slope)
            
            # 平均傾きと目標傾きの差を計算する
            mean_slope = np.mean(slopes)
            diff = abs(mean_slope - self.target_slope)
            
            # 最小の差を持つパラメータを選択する
            if diff < min_diff:
                min_diff = diff
                best_zipf_param = zipf_param
                best_slope = mean_slope
        
        return best_zipf_param, best_slope
    
    
    def generate_var_degrees(self, zipf_param: float) -> Dict[int, int]:
        """
        変数の出現頻度(次数)を生成
        
        Args:
            num_vars (int): 変数の数
            zipf_param (float): Zipfのパラメータ
        
        Returns:
            Dict[int, int]: {var_id: degree} 変数の出現頻度(次数)
        """
        
        # 変数IDと次数のペアを生成
        zipf_vars = np.random.zipf(zipf_param, self.num_vars)
        variables, counts = np.unique(zipf_vars, return_counts=True)
        var_degrees = {int(var): int(count) for var, count in zip(variables, counts)}
        
        # 次数の降順にソートして、分かりやすいように新しいIDをつける
        sorted_items = sorted(var_degrees.items(), key=lambda t: (-t[1], t[0]))
        
        return {new_id: degree for new_id, (_, degree) in enumerate(sorted_items)}