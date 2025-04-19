from fixout.interface.ttypes import FairMetric, FairMetricEnum

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from sklearn.preprocessing import binarize
from sklearn.metrics import confusion_matrix


def equalized_odds(cm0,cm1):
    """
    Calculates the equalized odds (EOD) fairness metric.
    
    Parameters
    ----------
    cm0 : array-like
        Confusion matrix for the unprivileged group.
    cm1 : array-like
        Confusion matrix for the privileged group.

    Returns
    -------
    metric : FairMetric
        The calculated equalized odds metric.
    
    """
    tn0, fp0, fn0, tp0 = cm0 # unprivileged 
    tn1, fp1, fn1, tp1 = cm1 # privileged
    metric = FairMetric()
    metric.type = FairMetricEnum.EOD
    metric.value = ( (tp0/(tp0+fn0)) + (fp0/(fp0+tn0)) ) - ( (tp1/(tp1+fn1)) + (fp1/(fp1+tn1)) )
    return metric

def demographic_parity(cm0,cm1):
    """
    Calculates the demographic parity (DP) fairness metric.
    
    Parameters
    ----------
    cm0 : array-like
        Confusion matrix for the unprivileged group.
    cm1 : array-like
        Confusion matrix for the privileged group.

    Returns
    -------
    metric : FairMetric
        The calculated demographic parity metric.

    """
    tn0, fp0, fn0, tp0 = cm0 # unprivileged 
    tn1, fp1, fn1, tp1 = cm1 # privileged
    metric = FairMetric()
    metric.type = FairMetricEnum.DP
    metric.value = ((tp0+tn0)/(tn0+fp0+fn0+tp0)) - ((tp1+tn1)/(tn1+fp1+fn1+tp1))
    return metric

def equal_opportunity(cm0,cm1):
    """
    Calculates the equal opportunity (EO) fairness metric.
    
    Parameters
    ----------
    cm0 : array-like
        Confusion matrix for the unprivileged group.
    cm1 : array-like
        Confusion matrix for the privileged group.

    Returns
    -------
    metric : FairMetric
        The calculated equal opportunity metric.

    """
    _, _, fn0, tp0 = cm0 # unprivileged 
    _, _, fn1, tp1 = cm1 # privileged
    metric = FairMetric()
    metric.type = FairMetricEnum.EO
    metric.value = (tp0/(tp0+fn0)) - (tp1/(tp1+fn1)) 
    return metric

def predictive_equality(cm0,cm1):
    """
    Calculates the equal predictive equality metric.

    Parameters
    ----------
    cm0 : array-like
        Confusion matrix for the unprivileged group.
    cm1 : array-like
        Confusion matrix for the privileged group.

    Returns
    -------
    metric : FairMetric
        The calculated predictive equality metric.
    """
    _, fp0, _, tp0 = cm0 # unprivileged 
    _, fp1, _, tp1 = cm1 # privileged
    metric = FairMetric()
    metric.type = FairMetricEnum.PE
    metric.value = (fp0/(fp0+tp0)) - (fp1/(fp1+tp1)) 
    return metric

def predictive_parity(cm0,cm1):
    """
    Computes the Predictive Parity (PP) fairness metric.

    Parameters
    ----------
    cm0 : array-like
        Confusion matrix for the unprivileged group.
    cm1 : array-like
        Confusion matrix for the privileged group.

    Returns
    -------
    FairMetric
        The calculated predictive parity metric.
    """
    _, fp0, _, tp0 = cm0 # unprivileged 
    _, fp1, _, tp1 = cm1 # privileged
    metric = FairMetric()
    metric.type = FairMetricEnum.PP
    metric.value = (tp0/(tp0+fp0)) - (tp1/(tp1+fp1))
    return metric

def conditional_accuracy_equality(cm0,cm1):
    """
    Computes the Conditional Accuracy Equality (CEA) fairness metric.

    Parameters
    ----------
    cm0 : array-like
        Confusion matrix for the unprivileged group.
    cm1 : array-like
        Confusion matrix for the privileged group.

    Returns
    -------
    FairMetric
        The calculated conditional accuracy equality metric.

    """
    tn0, fp0, fn0, tp0 = cm0 # unprivileged 
    tn1, fp1, fn1, tp1 = cm1 # privileged
    metric = FairMetric()
    metric.type = FairMetricEnum.CEA
    metric.value = ((tp0/(tp0+fp0))+(tn0/(tn0+fn0))) - ((tp1/(tp1+fp1))+(tn1/(tn1+fn1)))
    return metric



    
def computeFairnessMetrics(metrics, sFeature, X_test, y_test, y_pred):
    """
    Calculate fariness metrics for a given ensemble of instances. 
    
    Supported fariness metrics: Demographic Parity, Equal Opportunity, Predictive Equality.

    Check out the enum types : 'FairMetricEnum'
    
    Parameters
    ----------
    metrics : list
        List of fairness metric types to be calculated.

    sFeature : SensitiveFeature 
        Sensitive feature that will be take into account to calculate fairness metrics.

    X_test : array-like
        Feature matrix of the test set.
    
    y_test : array-like
        True labels of the test set.
    
    y_pred : array-like
        Predicted labels.

    Returns
    -------
    results : list of FairMetric
        List with all requested metrics calculated.
        Returns an empty list if no metric is informed or a problem when calculating the confusion matrix is found.

    """ 
    
    y_test_array = np.array(y_test)
    X_test_array = np.array(X_test)

    results = {}
    
    possible_values = list(set(X_test_array[:, sFeature.featureIndex])) # default = sFeature.unprivPop
    if len(possible_values) == 2:
        possible_values = possible_values[:-1]

    for value in possible_values: 

        results[str(value)] = []

        if sFeature.type == 0: # numeric sensitive feature
            sens_array = X_test_array[:, sFeature.featureIndex] 
            sens_array = binarize([sens_array.astype(float)],threshold=value)
        
        indexes0 = np.where(X_test_array[:, sFeature.featureIndex] == value)
        indexes1 = np.where(X_test_array[:, sFeature.featureIndex] != value) #sFeature.unprivPop
        
        y_test_0 = y_test_array[indexes0]
        y_test_1 = y_test_array[indexes1]
        y_pred_0 = y_pred[indexes0]
        y_pred_1 = y_pred[indexes1]

        # tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        cm0 = confusion_matrix(y_test_0, y_pred_0).ravel()
        cm1 = confusion_matrix(y_test_1, y_pred_1).ravel()

        if (len(cm0) == 4) and (len(cm1) == 4) :
            
            for i in metrics:
                if i == FairMetricEnum.DP:  
                    results[str(value)].append(demographic_parity(cm0,cm1))
                elif i == FairMetricEnum.EO:
                    results[str(value)].append(equal_opportunity(cm0,cm1))
                elif i == FairMetricEnum.PE:
                    results[str(value)].append(predictive_equality(cm0,cm1))
                elif i == FairMetricEnum.EOD:
                    results[str(value)].append(equalized_odds(cm0,cm1))
                elif i == FairMetricEnum.PP:
                    results[str(value)].append(predictive_parity(cm0,cm1))
                elif i == FairMetricEnum.CEA:
                    results[str(value)].append(conditional_accuracy_equality(cm0,cm1))
        
    return results
