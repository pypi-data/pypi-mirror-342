"""数据预处理模块"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from typing import List

class FeaturePreprocessor:
    """特征预处理类（归一化+离散系数计算）"""
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.discrete_coefficients = []  # 离散系数（标准差/均值）

    def fit(self, data: pd.DataFrame):
        """拟合预处理参数
        
        Args:
            data (pd.DataFrame): 输入数据（n_samples x n_features）
        """
        self.scaler.fit(data)
        mean = data.mean()
        std = data.std()
        self.discrete_coefficients = (std / abs(mean)).tolist()

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """应用预处理
        
        Args:
            data (pd.DataFrame): 输入数据
        
        Returns:
            pd.DataFrame: 归一化后的数据（乘以10缩放）
        """
        scaled_data = self.scaler.transform(data) * 10
        return pd.DataFrame(scaled_data, index=data.index, columns=data.columns)