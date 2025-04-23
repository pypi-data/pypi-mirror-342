"""KMDPC 工具函数：距离/密度计算"""
import pandas as pd
import numpy as np
import math as ma
from typing import List, Dict

def calculate_distance_matrix(
    data: pd.DataFrame, 
    statistic: List[float], 
    n_features: int
) -> pd.DataFrame:
    """生成带权重的欧氏距离矩阵
    
    Args:
        data (pd.DataFrame): 预处理后的数据（索引为1-based样本编号）
        statistic (List[float]): 各特征的离散系数
        n_features (int): 特征维度
    
    Returns:
        pd.DataFrame: n_samples x n_samples 距离矩阵
    """
    n_samples = len(data)
    distance_matrix = pd.DataFrame(index=range(1, n_samples+1), columns=range(1, n_samples+1))
    for i in range(1, n_samples + 1):
        for j in range(1, n_samples + 1):
            distance = 0.0
            for d in range(n_features):
                weight = statistic[d]
                diff = data.iloc[i-1, d] - data.iloc[j-1, d]
                distance += weight * (diff ** 2)
            distance_matrix.loc[i, j] = ma.sqrt(distance)
    return distance_matrix

def compute_local_density(
    distance_matrix: pd.DataFrame, 
    dc: float
) -> pd.DataFrame:
    """计算局部密度（高斯核函数）
    
    Args:
        distance_matrix (pd.DataFrame): 距离矩阵
        dc (float): 截断距离
    
    Returns:
        pd.DataFrame: 包含局部密度的DataFrame（索引为样本编号，列'ρ'）
    """
    density = pd.DataFrame(index=distance_matrix.index, columns=['ρ'])
    for i in distance_matrix.index:
        d_i = distance_matrix.loc[i, :].values
        density.loc[i, 'ρ'] = np.sum(np.exp(-(d_i ** 2) / (dc ** 2)))
    return density

def compute_high_density_distance(
    density: pd.DataFrame, 
    distance_matrix: pd.DataFrame
) -> pd.DataFrame:
    """计算局部最高密度距离
    
    Args:
        density (pd.DataFrame): 局部密度
        distance_matrix (pd.DataFrame): 距离矩阵
    
    Returns:
        pd.DataFrame: 包含高密距离的DataFrame（索引为样本编号，列'δ'）
    """
    high_density_dist = pd.DataFrame(index=density.index, columns=['δ'])
    sorted_indices = density.sort_values(by='ρ', ascending=False).index.tolist()
    
    for i in sorted_indices:
        if i == sorted_indices[0]:  # 密度最高的点，距离设为最大距离
            high_density_dist.loc[i, 'δ'] = distance_matrix.loc[i, :].max()
        else:
            # 找密度更高的点中最近的距离
            higher_density_points = density[density['ρ'] > density.loc[i, 'ρ']].index
            if not higher_density_points.empty:
                min_dist = distance_matrix.loc[i, higher_density_points].min()
                high_density_dist.loc[i, 'δ'] = min_dist
            else:  # 理论上不会发生
                high_density_dist.loc[i, 'δ'] = 0.0
    return high_density_dist