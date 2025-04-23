# kmdpc/utils.py
import pandas as pd
import numpy as np
import math as ma
from typing import List, Tuple

def calculate_discrete_coefficients(data: pd.DataFrame) -> List[float]:
    """计算特征离散系数（标准差/均值）"""
    mean = data.mean()
    std = data.std()
    return (std / abs(mean)).tolist()

def distance(i: int, j: int, n: int, statistic: List[float], data: pd.DataFrame) -> float:
    """带权重的欧氏距离计算"""
    result = 0.0
    for d in range(n):
        weight = statistic[d]
        diff = data.iloc[i-1, d] - data.iloc[j-1, d]  # 修正索引从0开始
        result += weight * (diff ** 2)
    return ma.sqrt(result)

def distance_matrix(n: int, dem: int, statistic: List[float], data: pd.DataFrame) -> pd.DataFrame:
    """生成距离矩阵"""
    distance_in_total = pd.DataFrame(index=range(1, n+1), columns=range(1, n+1))
    for i in range(1, n+1):
        for j in range(1, n+1):
            distance_in_total.loc[i, j] = distance(i, j, dem, statistic, data)
    return distance_in_total

def local_density(d_i: np.ndarray, d_c: float) -> float:
    """计算局部密度（高斯核）"""
    return np.sum(np.exp(-(d_i ** 2) / (d_c ** 2)))

def high_density_distance(
    density_local: pd.DataFrame, 
    distance_matrix: pd.DataFrame, 
    n: int
) -> pd.DataFrame:
    """计算局部最高密度距离"""
    high_den = pd.DataFrame(index=range(1, n+1), columns=['δ'])
    sorted_indices = density_local.sort_values(by='ρ', ascending=False).index.tolist()
    
    for i in range(1, n+1):
        if i == sorted_indices[0]:  # 密度最高的点，距离设为最大距离
            high_den.loc[i, 'δ'] = distance_matrix.loc[i, :].max()
        else:
            # 找密度比当前点高的最近点
            higher_density_points = density_local[density_local['ρ'] > density_local.loc[i, 'ρ']].index
            if not higher_density_points.empty:
                min_dist = distance_matrix.loc[i, higher_density_points].min()
                high_den.loc[i, 'δ'] = min_dist
            else:  # 不存在更高密度点（理论上不会发生）
                high_den.loc[i, 'δ'] = 0.0
    return high_den