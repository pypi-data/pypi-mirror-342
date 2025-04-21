import numpy as np
import shap
import pandas as pd
from typing import Tuple, Union, List, Literal


class GWRExplain:
    """
    A class for computing SHAP values based on local regression coefficients and neighborhood samples.
    Supports 'interventional' method and explanations using shap.LinearExplainer.

    Attributes
    ----------
    shap_values : pd.DataFrame
        SHAP values for each feature of each sample.
    """

    def __init__(self):
        self.shap_values: Union[pd.DataFrame, None] = None

    def explain(
        self,
        X: pd.DataFrame,
        y: pd.DataFrame,
        coefficients: pd.DataFrame,
        neighbors: List[np.ndarray],
        feature_perturbation: Literal['interventional', 'independent']
    ) -> pd.DataFrame:
        """
        Compute SHAP values based on local regression coefficients and neighborhood samples.

        Parameters
        ----------
        X : pd.DataFrame
            Feature data, with the same number of rows as in the coefficients.
        y : pd.Series
            Target variable data, with the same number of rows as in the coefficients.
        coefficients : pd.DataFrame
            Local regression coefficients, including the 'intercept' column and other feature columns.
        neighbors : List[np.ndarray]
            Indices of neighborhood samples (neighbor indices).
        feature_perturbation : Literal['interventional', 'independent']
            Feature perturbation method: 'interventional' or 'independent'.
        """

        if 'intercept' not in coefficients.columns:
            raise ValueError("coefficients DataFrame must contain an 'intercept' column.")

        feature_names = [col for col in coefficients.columns if col != 'intercept']
        shap_values = []

        for idx, row in coefficients.iterrows():
            neighbor_idx = neighbors[idx]
            if neighbor_idx is None or len(neighbor_idx) == 0:
                raise ValueError(f"No neighbors found for index {idx}.")

            X_neighbor = X.iloc[neighbor_idx]

            if feature_perturbation == 'interventional':
                neighbor_mean = X_neighbor.mean(axis=0)
                diff = X_neighbor.iloc[0, :] - neighbor_mean
                sv = diff * row[feature_names].values
            else:
                model_tuple = (row[feature_names].values.reshape(1, -1), row['intercept'])
                explainer = shap.LinearExplainer(
                    model=model_tuple,
                    data=X_neighbor,
                    feature_perturbation=feature_perturbation
                )
                sv = explainer.shap_values(X_neighbor)[0, :]

            shap_values.append(sv)

        self.shap_values = pd.DataFrame(np.vstack(shap_values), columns=feature_names)
        # return self.shap_values