import numpy as np
import pandas as pd
import math as ma
from operator import itemgetter
from .utils import distance_workout, density_workout, high_denworkout, cluster_density_core

class KMDPCCluster:
    """KMDPC聚类算法核心类
    
    Attributes:
        attri (int): 特征维度
        k (int): 聚类数
        dc (float): 截断距离
        core (list): 聚类中心样本索引
        class_result (pd.DataFrame): 聚类结果
    """
    
    def __init__(self, attri: int, k: int):
        self.attri = attri
        self.k = k
        self.dc = None
        self.core = []
        self.class_result = None

    def fit(self, data: pd.DataFrame, y_true: pd.Series):
        """拟合数据并执行聚类
        
        Args:
            data (pd.DataFrame): 输入数据（特征矩阵）
            y_true (pd.Series): 真实标签（用于评估，非必需）
        """
        # 数据预处理（假设已标准化，代码中需添加预处理接口）
        origin_data = self._preprocess(data)
        
        # 计算距离矩阵
        distance_in_total = distance_workout(len(origin_data), self.attri)
        
        # 计算局部密度和高密距离
        self.dc = self._determine_dc(distance_in_total)
        density_local = density_workout(distance_in_total, len(origin_data), self.dc)
        high_den = high_denworkout(density_local, distance_in_total, len(origin_data))
        
        # 确定聚类中心
        self.core, _ = cluster_density_core(len(origin_data), density_local, high_den)
        
        # 生成初始聚类结果
        self.class_result = self._cluster_result(len(origin_data), self.core, density_local)
        
        # 优化分配策略（KMDPC迭代）
        for _ in range(10):
            self.class_result = self._kmdpc_optimization(self.class_result, self.attri, origin_data)

    def _preprocess(self, data: pd.DataFrame) -> pd.DataFrame:
        """特征标准化及离散系数计算（内部使用）"""
        # 添加标准化逻辑（示例中假设输入已标准化，可扩展为自动处理）
        return data.copy()

    def _determine_dc(self, distance_matrix: pd.DataFrame) -> float:
        """自动确定截断距离dc"""
        arr = distance_matrix.values.flatten()
        arr.sort()
        return arr[int(len(arr) * 0.02 + len(arr)**0.5)]  # 经验公式，可优化
    
    def _cluster_result(self, n: int, core: list, density_local: pd.DataFrame) -> pd.DataFrame:
        """生成初始聚类结果（内部使用）"""
        # 简化后的聚类分配逻辑（需与原代码逻辑一致）
        result = pd.DataFrame(index=density_local.index, columns=['result'])
        # ... 原代码中的cluster_result逻辑 ...
        return result

    def _kmdpc_optimization(self, class_result: pd.DataFrame, attri: int, data: pd.DataFrame) -> pd.DataFrame:
        """KMDPC优化分配策略（内部使用）"""
        # ... 原代码中的KMDPC逻辑 ...
        return class_result