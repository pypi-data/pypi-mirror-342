import pandas as pd
from ._custom_disparity_metric import custom_disparity_metric as custom_disparity_metric
from solas_disparity.types import DifferenceCalculation as DifferenceCalculation, Disparity as Disparity, DisparityCalculation as DisparityCalculation, RatioCalculation as RatioCalculation
from typing import List, Optional

def precision(group_data: pd.DataFrame, protected_groups: List[str], reference_groups: List[str], group_categories: List[str], outcome: pd.Series, label: pd.Series, ratio_threshold: float, difference_threshold: float, sample_weight: Optional[pd.Series] = ...) -> Disparity: ...
