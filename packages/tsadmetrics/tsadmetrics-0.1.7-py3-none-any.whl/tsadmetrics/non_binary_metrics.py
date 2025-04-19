import numpy as np
from ._tsadeval.metrics import *
from .metric_utils import transform_to_full_series
from sklearn.metrics import auc
from .binary_metrics import point_adjusted_precision, point_adjusted_recall, segment_wise_precision, segment_wise_recall
from pate.PATE_metric import PATE
def precision_at_k(y_true : np.array ,y_anomaly_scores:  np.array):
    
    m = PatK_pw(y_true,y_anomaly_scores)

    return m.get_score()

def auc_roc_pw(y_true : np.array ,y_anomaly_scores:  np.array):
    
    m = AUC_ROC(y_true,y_anomaly_scores)

    return m.get_score()


def auc_pr_pw(y_true : np.array ,y_anomaly_scores:  np.array):
    
    m = AUC_PR_pw(y_true,y_anomaly_scores)

    return m.get_score()



def auc_pr_pa(y_true: np.array, y_anomaly_scores: np.array):
    thresholds = np.unique(y_anomaly_scores)[::-1]  # Descending order
    precisions = [1]
    recalls = [0]
    for t in thresholds[:-1]:

        y_pred = (y_anomaly_scores >= t).astype(int)


        precisions.append(point_adjusted_precision(y_true, y_pred))
        recalls.append(point_adjusted_recall(y_true, y_pred))
    
    recalls.append(1)
    precisions.append(0)
    auc_value = auc(recalls, precisions)
    return auc_value




def auc_pr_sw(y_true: np.array, y_anomaly_scores: np.array):
    thresholds = np.unique(y_anomaly_scores)[::-1]  # Descending order
    precisions = [1]
    recalls = [0]
    
    for t in thresholds[:-1]:
        y_pred = (y_anomaly_scores >= t).astype(int)
        precisions.append(segment_wise_precision(y_true, y_pred))
        recalls.append(segment_wise_recall(y_true, y_pred))
    recalls.append(1)
    precisions.append(0)
    auc_value = auc(recalls, precisions)
    return auc_value


def vus_roc(y_true : np.array ,y_anomaly_scores:  np.array, window=4):
    
    m = VUS_ROC(y_true,y_anomaly_scores,max_window=window)

    return m.get_score()


def vus_pr(y_true : np.array ,y_anomaly_scores:  np.array,  window=4):
    
    m = VUS_PR(y_true,y_anomaly_scores,max_window=window)

    return m.get_score()


def real_pate(y_true: np.array, y_anomaly_scores: np.array, early: int, delay: int):
    """
    Calculate PATE score for anomaly detection in time series.
    The PATE score is the ratio of the number of true positives to the sum of true positives, false positives, and false negatives, within a given early and delay range.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_anomaly_scores (np.array): The predicted binary labels for the time series data.
    early (int): The maximum number of time steps before an anomaly must be predicted to be considered early.
    delay (int): The maximum number of time steps after an anomaly must be predicted to be considered delayed.

    Returns:
    float: The PATE score.
    """
    
    return PATE(y_true, y_anomaly_scores, early, delay, binary_scores=False)