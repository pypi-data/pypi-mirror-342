from sklearn.metrics import accuracy_score, normalized_mutual_info_score, adjusted_rand_score
import numpy as np

def purity_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """纯度分数计算
    
    Args:
        y_true (np.ndarray): 真实标签
        y_pred (np.ndarray): 预测聚类标签
        
    Returns:
        float: 纯度分数
    """
    y_voted_labels = np.zeros_like(y_true)
    labels = np.unique(y_true)
    ordered_labels = np.arange(len(labels))
    for k, lbl in enumerate(labels):
        y_true[y_true == lbl] = ordered_labels[k]
    bins = np.concatenate((ordered_labels, [np.max(ordered_labels) + 1]))
    
    for cluster in np.unique(y_pred):
        hist, _ = np.histogram(y_true[y_pred == cluster], bins=bins)
        winner = np.argmax(hist)
        y_voted_labels[y_pred == cluster] = winner
    
    return accuracy_score(y_true, y_voted_labels)