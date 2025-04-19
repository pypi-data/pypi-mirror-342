import numpy as np
from .metric_utils import *
from .metric_utils import get_events, calculate_intersection


from ._tsadeval.metrics import *
from ._tsadeval.prts.basic_metrics_ts import ts_fscore
from pate.PATE_metric import PATE
def point_wise_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate point-wise recall for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The point-wise recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    m = Pointwise_metrics(len(y_true),y_true,y_pred)
    m.set_confusion()
    TP,FN = m.tp,m.fn
    #TP, _, FP, FN = get_tp_tn_fp_fn_point_wise(y_true, y_pred)
    if TP == 0:
        return 0
    return TP / (TP + FN)

def point_wise_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate point-wise precision for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The point-wise precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    #TP, _, FP, FN = get_tp_tn_fp_fn_point_wise(y_true, y_pred)
    m = Pointwise_metrics(len(y_true),y_true,y_pred)
    m.set_confusion()
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def point_wise_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate point-wise F-score for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    betha (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The point-wise F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = point_wise_precision(y_true, y_pred)
    recall = point_wise_recall(y_true, y_pred)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def point_adjusted_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate point-adjusted recall for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The point-adjusted recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = PointAdjust(len(y_true),y_true,y_pred)
    #m.adjust()
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def point_adjusted_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate point-adjusted precision for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The point-adjusted precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = PointAdjust(len(y_true),y_true,y_pred)
    #m.adjust()
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def point_adjusted_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate point-adjusted F-score for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The point-adjusted F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = point_adjusted_precision(y_true, y_pred)
    recall = point_adjusted_recall(y_true, y_pred)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)



def delay_th_point_adjusted_recall(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate delay thresholded point-adjusted recall for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (int): The maximum number of time steps within which an anomaly must be predicted to be considered detected.

    Returns:
    float: The delay thresholded point-adjusted recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = DelayThresholdedPointAdjust(len(y_true),y_true,y_pred,k=k)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def delay_th_point_adjusted_precision(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate delay thresholded point-adjusted precision for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (int): The maximum number of time steps within which an anomaly must be predicted to be considered detected.

    Returns:
    float: The delay thresholded point-adjusted precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = DelayThresholdedPointAdjust(len(y_true),y_true,y_pred,k=k)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def delay_th_point_adjusted_f_score(y_true: np.array, y_pred: np.array, k: int, beta=1):
    """
    Calculate delay thresholded point-adjusted F-score for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (int): The maximum number of time steps within which an anomaly must be predicted to be considered detected.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The delay thresholded point-adjusted F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = delay_th_point_adjusted_precision(y_true, y_pred, k)
    recall = delay_th_point_adjusted_recall(y_true, y_pred, k)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def point_adjusted_at_k_recall(y_true: np.array, y_pred: np.array, k: float):
    """
    Calculate k percent point-adjusted at K% recall for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (float): The minimum percentage of the anomaly that must be detected to consider the anomaly as detected.

    Returns:
    float: The point-adjusted recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    #TP, _, FP, FN = get_tp_tn_fp_fn_point_adjusted_at_k(y_true, y_pred, k)
    m = PointAdjustKPercent(len(y_true),y_true,y_pred,k=k)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def point_adjusted_at_k_precision(y_true: np.array, y_pred: np.array, k: float):
    """
    Calculate point-adjusted at K% precision for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (float): The minimum percentage of the anomaly that must be detected to consider the anomaly as detected.

    Returns:
    float: The point-adjusted precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    #TP, _, FP, _ = get_tp_tn_fp_fn_point_adjusted_at_k(y_true, y_pred, k)
    m = PointAdjustKPercent(len(y_true),y_true,y_pred,k=k)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def point_adjusted_at_k_f_score(y_true: np.array, y_pred: np.array, k: float, beta=1):
    """
    Calculate point-adjusted at K% F-score for anomaly detection in time series.
    Implementation of https://link.springer.com/article/10.1007/s10618-023-00988-8

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (float): The minimum percentage of the anomaly that must be detected to consider the anomaly as detected.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The point-adjusted F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    precision = point_adjusted_at_k_precision(y_true, y_pred, k)
    recall = point_adjusted_at_k_recall(y_true, y_pred, k)

    if precision == 0 or recall == 0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def latency_sparsity_aw_recall(y_true: np.array, y_pred: np.array, ni: int):
    """
    Calculate latency and sparsity aware recall for anomaly detection in time series.
    Implementation of https://dl.acm.org/doi/10.1145/3447548.3467174

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    ni (int): The batch size used in the implementation to handle latency and sparsity.

    Returns:
    float: The latency and sparsity aware recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = LatencySparsityAware(len(y_true),y_true,y_pred,tw=ni)
    TP,FN = m.tp, m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def latency_sparsity_aw_precision(y_true: np.array, y_pred: np.array, ni: int):
    """
    Calculate latency and sparsity aware precision for anomaly detection in time series.
    Implementation of https://dl.acm.org/doi/10.1145/3447548.3467174

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    ni (int): The batch size used in the implementation to handle latency and sparsity.

    Returns:
    float: The latency and sparsity aware precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = LatencySparsityAware(len(y_true),y_true,y_pred,tw=ni)
    TP,FP = m.tp, m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def latency_sparsity_aw_f_score(y_true: np.array, y_pred: np.array, ni: int, beta=1):
    """
    Calculate latency and sparsity aware F-score for anomaly detection in time series.
    Implementation of https://dl.acm.org/doi/10.1145/3447548.3467174

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    ni (int): The batch size used in the implementation to handle latency and sparsity.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The latency and sparsity aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0

    recall = latency_sparsity_aw_recall(y_true,y_pred,ni)
    precision = latency_sparsity_aw_precision(y_true,y_pred,ni)
    if precision == 0 or recall == 0:
        return 0
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)

    
def segment_wise_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate segment-wise recall for anomaly detection in time series.
    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The segment-wise recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    #TP, _, FN = get_tp_fp_fn_segment_wise(y_true, y_pred)
    m = Segmentwise_metrics(len(y_true),y_true,y_pred)
    TP,FN = m.tp,m.fn
    if TP == 0:
        return 0
    return TP / (TP + FN)

def segment_wise_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate segment-wise precision for anomaly detection in time series.
    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The segment-wise precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    #TP, FP, _ = get_tp_fp_fn_segment_wise(y_true, y_pred)
    m = Segmentwise_metrics(len(y_true),y_true,y_pred)
    TP,FP = m.tp,m.fp
    if TP == 0:
        return 0
    return TP / (TP + FP)

def segment_wise_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate segment-wise F-score for anomaly detection in time series.
    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The segment-wise F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
  
    """
    m = Segmentwise_metrics(len(y_true),y_true,y_pred)
    TP,FN,FP = m.tp,m.fn,m.fp
    if TP==0:
        return 0
    
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    
    if precision == 0 or recall == 0:
        return 0
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)

def composite_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate composite F-score for anomaly detection in time series.
    Implementation of https://ieeexplore.ieee.org/document/9525836

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The composite F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
  
    """
    m = Composite_f(len(y_true),y_true,y_pred)
    #Point wise precision
    precision =  m.precision()#point_wise_precision(y_true,y_pred)

    #Segment wise recall
    recall = m.recall()#segment_wise_recall(y_true,y_pred)

    if precision==0 or recall==0:
        return 0

    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)

def time_tolerant_recall(y_true: np.array, y_pred: np.array, t: int) -> float:
    """
    Calculate time tolerant recall for anomaly detection in time series.
    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    t (int): The time tolerance parameter

    Returns:
    float: The time tolerant recall score, which is the ratio of true positives to the sum of true positives and false negatives.
    """
    if np.sum(y_pred) == 0:
        return 0
    
    m = Time_Tolerant(len(y_true),y_true,y_pred,d=t)
    return m.recall()

def time_tolerant_precision(y_true: np.array, y_pred: np.array, t: int) -> float:
    """
    Calculate time tolerant precision for anomaly detection in time series.
    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    t (int): The time tolerance parameter

    Returns:
    float: The time tolerant precision score, which is the ratio of true positives to the sum of true positives and false positives.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Time_Tolerant(len(y_true),y_true,y_pred, d=t)
    return m.precision()


def time_tolerant_f_score(y_true: np.array, y_pred: np.array,t: int, beta=1):
    """
    Calculate time tolerant F-score for anomaly detection in time series.
    Implementation of https://arxiv.org/pdf/1802.04431

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    t (int): The time tolerance parameter
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.
    
    Returns:
    float: The time tolerant F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
  
    """
    precision = time_tolerant_precision(y_true,y_pred,t)
    recall = time_tolerant_recall(y_true,y_pred,t)
    if precision==0 or recall==0:
        return 0
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)


def range_based_recall(y_true: np.array, y_pred: np.array, alpha: float, bias='flat', cardinality_mode='one'):
    """
    Calculate range-based recall for anomaly detection in time series.
    
    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    bias (str): The type of bias to apply for weighting (flat, front-end, back-end, middle).
    cardinality (str, optional): ["one", "reciprocal", "udf_gamma"]. Defaults to "one".
    
    Returns:
    float: The range-based recall score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Range_PR(len(y_true),y_true,y_pred,cardinality=cardinality_mode, alpha=alpha,bias=bias)
    return m.recall()



def range_based_precision(y_true: np.array, y_pred: np.array, alpha: float, bias='flat', cardinality_mode='one'):
    """
    Calculate range-based precision for anomaly detection in time series.
    
    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    bias (str): The type of bias to apply for weighting (flat, front-end, back-end, middle).
    cardinality (str, optional): ["one", "reciprocal", "udf_gamma"]. Defaults to "one".
    
    Returns:
    float: The range-based precision score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Range_PR(len(y_true),y_true,y_pred,cardinality=cardinality_mode, alpha=alpha,bias=bias)
    return m.precision()
    
    
    



def range_based_f_score(y_true: np.array, y_pred: np.array, p_alpha: float, r_alpha: float,  p_bias='flat', r_bias='flat', cardinality_mode='one', beta=1) -> float:
    """
    Calculate range-based F-score for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    p_bias: string, default="flat"
            Positional bias for precision. This should be "flat", "front", "middle", or "back"
    r_bias: string, default="flat"
        Positional bias for recall. This should be "flat", "front", "middle", or "back"
    cardinality_mode (str, optional): ["one", "reciprocal", "udf_gamma"]. Defaults to "one".
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The range-based F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    f = ts_fscore(y_true, y_pred, beta=beta, p_alpha=p_alpha, r_alpha=r_alpha, cardinality=cardinality_mode, p_bias=p_bias, r_bias=r_bias)
    return f




def ts_aware_recall(y_true: np.array, y_pred: np.array, alpha: float, delta: float, theta: float, past_range: bool = False):
    """
    Calculate time series aware recall for anomaly detection in time series.
    
    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    past_range: Determines if the range is considered in the past or future as specified in https://www.mdpi.com/2079-9292/11/8/1213
    
    Returns:
    float: The time series aware recall score.
    """
    m = TaF(len(y_true),y_true,y_pred,alpha=alpha,theta=theta,delta=delta,past_range=past_range)
    return m.recall()




def ts_aware_precision(y_true: np.array, y_pred: np.array,alpha: float, delta: float, theta: float, past_range: bool = False):
    """
    Calculate time series aware precision for anomaly detection in time series.
    
    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    past_range: Determines if the range is considered in the past or future as specified in https://www.mdpi.com/2079-9292/11/8/1213
    
    Returns:
    float: The time series aware precision score.
    """
    m = TaF(len(y_true),y_true,y_pred,alpha=alpha,theta=theta,delta=delta,past_range=past_range)
    return m.precision()

    



def ts_aware_f_score(y_true: np.array, y_pred: np.array, beta: float, alpha: float, delta: float, theta: float, past_range: bool = False):
    """
    Calculate time series aware F-score for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.
    past_range: Determines if the range is considered in the past or future as specified in https://www.mdpi.com/2079-9292/11/8/1213

    Returns:
    float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    
    m = TaF(len(y_true),y_true,y_pred,alpha=alpha,theta=theta,delta=delta,past_range=past_range)
    precision = m.precision()
    recall = m.recall()
    if precision==0 or recall==0:
        return 0
    
    return ((1 + beta**2) * precision * recall) / (beta**2 * precision + recall)





def enhanced_ts_aware_recall(y_true: np.array, y_pred: np.array, theta: float):
    """
    Calculate enhanced time series aware recall for anomaly detection in time series.
    
    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    
    Returns:
    float: The time series aware recall score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = eTaF(len(y_true),y_true,y_pred,theta_p=theta)
    return m.recall()




def enhanced_ts_aware_precision(y_true: np.array, y_pred: np.array, theta: float):
    """
    Calculate enhanced time series aware precision for anomaly detection in time series.
    
    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    alpha (float): A parameter that controls the length of the range considered for true positives.
    
    Returns:
    float: The time series aware precision score.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = eTaF(len(y_true),y_true,y_pred,theta_p=theta)
    return m.precision()

    



def enhanced_ts_aware_f_score(y_true: np.array, y_pred: np.array, beta: float, theta_p: float, theta_r: float):
    """
    Calculate enhanced time series aware F-score for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = eTaF(len(y_true),y_true,y_pred,theta_p=theta_p, theta_r=theta_r)
    return m.result['f1']



def affiliation_based_recall(y_true: np.array, y_pred: np.array):
    """
    Calculate affiliation based recall for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Affiliation(len(y_true),y_true,y_pred)
    s = m.get_score()
    return m.r


def affiliation_based_precision(y_true: np.array, y_pred: np.array):
    """
    Calculate affiliation based F-score for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Affiliation(len(y_true),y_true,y_pred)
    s = m.get_score()
    return m.p


def affiliation_based_f_score(y_true: np.array, y_pred: np.array, beta=1):
    """
    Calculate affiliation based F-score for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    beta (float): The beta value, which determines the weight of precision in the combined score.
                  Default is 1, which gives equal weight to precision and recall.

    Returns:
    float: The time series aware F-score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    if np.sum(y_pred) == 0:
        return 0
    m = Affiliation(len(y_true),y_true,y_pred)
    return m.get_score(beta)


def nab_score(y_true: np.array, y_pred: np.array):
    """
    Calculate NAB score for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.


    Returns:
    float: The nab score, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    
    m = NAB_score(len(y_true),y_true,y_pred)
    return m.get_score()

def temporal_distance(y_true: np.array, y_pred: np.array, distance: int = 0):
    """
    Calculate temporal distane for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    distance (int): The distance type parameter for the temporal distance calculation.
        0: Euclidean distance
        1: Squared Euclidean distance


    Returns:
    float: The temporal distance, which is the harmonic mean of precision and recall, adjusted by the beta value.
    """
    
    m = Temporal_Distance(len(y_true),y_true,y_pred,distance=distance)
    return m.get_score()

def average_detection_count(y_true: np.array, y_pred: np.array):
    """
    Calculate average detection count for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.


    Returns:
    float: The average detection count.
    """
    
    b = Binary_detection(len(y_true),y_true,y_pred)
    azs = b.get_gt_anomalies_segmentwise()
    a_points = b.get_gt_anomalies_ptwise()

    counts = []
    for az in azs:
        count = 0
        for ap in a_points:
            if ap >= az[0] and ap <= az[1]:
                count+=1
        counts.append(count)
    
    return np.mean(counts)

def absolute_detection_distance(y_true: np.array, y_pred: np.array):
    """
    Calculate absolute detection distance for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.


    Returns:
    float: The absolute detection distance.
    """
    
    b = Binary_detection(len(y_true),y_true,y_pred)
    azs = b.get_gt_anomalies_segmentwise()
    a_points = b.get_gt_anomalies_ptwise()

    distance = 0
    for az in azs:
        for ap in a_points:
            if ap >= az[0] and ap <= az[1]:
                center = int((az[0] + az[1]) / 2)
                distance+=abs(ap - center)
    
    return distance/len(a_points)


def total_detected_in_range(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate total detected in range for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (int): The maximum number of time steps within which an anomaly must be predicted to be considered detected.

    Returns:
    float: The total detected in range.
    """
    if np.sum(y_pred) == 0:
        return 0
    em,da,ma,_ = counting_method(y_true, y_pred, k)

    
    return (em + da)/(em + da + ma)


def detection_accuracy_in_range(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate detection accuracy in range for anomaly detection in time series.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (int): The maximum number of time steps within which an anomaly must be predicted to be considered detected.

    Returns:
    float: The total detected in range.
    """
    if np.sum(y_pred) == 0:
        return 0
    em,da,_,fa = counting_method(y_true, y_pred, k)

    
    return (em + da)/(em + da + fa)


def weighted_detection_difference(y_true: np.array, y_pred: np.array, k: int):
    """
    Calculate weighted detection difference for anomaly detection in time series.
    The weighted detection difference is the difference between the number of true positives and the number of false positives, weighted by the number of true positives.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    k (int): The maximum number of time steps within which an anomaly must be predicted to be considered detected.

    Returns:
    float: The weighted detection difference.
    """
    if np.sum(y_pred) == 0:
        return 0
    
    def gaussian(dt,tmax):
        if dt < tmax:
            return 1- dt/tmax
        else:
            return -1

    tmax = len(y_true)
    
    ones_indices = np.where(y_true == 1)[0]
    
    y_modified = y_true.astype(float).copy()
    
    for i in range(len(y_true)):
        if y_true[i] == 0:
            dt = np.min(np.abs(ones_indices - i)) if len(ones_indices) > 0 else tmax
            y_modified[i] = gaussian(dt, tmax)
    
    ws = 0
    wf = 0
    for i in range(len(y_pred)):
        if y_pred[i] != 1:
            ws+=y_modified[i]
        else:
            wf+=y_modified[i]

    _,_,_,fa = counting_method(y_true, y_pred, k)

    
    return ws - wf*fa


def binary_pate(y_true: np.array, y_pred: np.array, early: int, delay: int):
    """
    Calculate PATE score for anomaly detection in time series.
    The PATE score is the ratio of the number of true positives to the sum of true positives, false positives, and false negatives, within a given early and delay range.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.
    early (int): The maximum number of time steps before an anomaly must be predicted to be considered early.
    delay (int): The maximum number of time steps after an anomaly must be predicted to be considered delayed.

    Returns:
    float: The PATE score.
    """
    
    return PATE(y_true, y_pred, early, delay, binary_scores=True)

def mean_time_to_detect(y_true: np.array, y_pred: np.array):
    """
    Calculate mean time to detect for anomaly detection in time series.
    The mean time to detect is the average number of time steps between the ground truth anomaly and the predicted anomaly.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_pred (np.array): The predicted binary labels for the time series data.

    Returns:
    float: The mean time to detect.
    """
    
    b = Binary_detection(len(y_true),y_true,y_pred)
    a_events = b.get_gt_anomalies_segmentwise()
    t_sum = 0
    for _,b in a_events:
        for i in range(b,len(y_pred)):
            if y_pred[i] == 1:
                t_sum+=i-b
                break
    
    return t_sum/len(a_events)
