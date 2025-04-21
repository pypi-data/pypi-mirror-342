import shap
import numpy as np
import pandas as pd
from shap.explainers._explainer import Explanation
from typing import Tuple, Union, List

def gwr_shap_summary_plot(
    shap_values: pd.DataFrame,
    X: Union[np.ndarray, pd.DataFrame],
    plot_type: str = "bar" or "dot"
) -> None:
    """
    Plot a global SHAP feature importance plot (bar or dot plot)

    Parameters:
        shap_values (shap.Explanation): SHAP explanation object computed from the model
        X (DataFrame or ndarray): Feature data
        plot_type (str): Choose between "bar" or "dot"

    Example:
        gwr_shap_summary_plot(shap_values, X, plot_type="dot")
    """
    assert plot_type in ["bar", "dot"], "plot_type must be 'bar' or 'dot'"
    assert shap_values.shape[0] == X.shape[0], "shap_values and X must have the same number of samples"
    assert shap_values.shape[1] == X.shape[1], "shap_values and X must have the same number of features"
    shap.summary_plot(shap_values.values, X, feature_names=shap_values.columns, plot_type=plot_type)

def gwr_shap_local_plot(
    shap_values: pd.DataFrame,
    X: Union[np.ndarray, pd.DataFrame],
    model_param: pd.DataFrame,
    feature_names: List[str],
    sample_index: int = 0
) -> None:
    """
    Visualize the SHAP waterfall plot for a single sample

    Parameters:
        shap_values (np.ndarray): SHAP values, shape (n_samples, n_features)
        X (np.ndarray): Input feature data
        model_param: Fitted model parameters, must include an 'intercept' column (scalar or vector)
        feature_names (List[str]): Feature names
        sample_index (int): Index of the sample to explain
    """
    
    # base_values = float(model_param['intercept'].iloc[sample_index])  # intercept
    base_values = np.tile(model_param['intercept'], len(X))  # intercept
    if(isinstance(X, pd.DataFrame)):
        feature_names = X.columns.tolist()
    else:
        if(feature_names is None):
            raise ValueError("feature_names must be provided if X is not a DataFrame")
        feature_names = feature_names

    explanation = Explanation(
        shap_values.values,
        base_values=base_values,
        data=X,
        feature_names=feature_names
    )
    shap.plots.waterfall(explanation[sample_index])