"""聚类评估指标"""
import numpy as np
from sklearn.metrics import accuracy_score, normalized_mutual_info_score, adjusted_rand_score

def purity_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """计算纯度分数
    
    Args:
        y_true (np.ndarray): 真实标签（n_samples,）
        y_pred (np.ndarray): 预测标签（n_samples,）
    
    Returns:
        float: 纯度分数（范围[0,1]）
    """
    y_voted = np.zeros_like(y_true)
    true_labels = np.unique(y_true)
    pred_clusters = np.unique(y_pred)
    
    # 映射真实标签为连续整数
    true_label_map = {lbl: idx for idx, lbl in enumerate(true_labels)}
    y_true_mapped = np.array([true_label_map[lbl] for lbl in y_true])
    
    for cluster in pred_clusters:
        mask = (y_pred == cluster)
        hist, _ = np.histogram(y_true_mapped[mask], bins=len(true_labels)+1)
        winner = np.argmax(hist)
        y_voted[mask] = winner
    
    return accuracy_score(y_true_mapped, y_voted)

# 其他指标（直接调用scikit-learn，保持兼容性）
accuracy_score = accuracy_score
normalized_mutual_info_score = normalized_mutual_info_score
adjusted_rand_score = adjusted_rand_score