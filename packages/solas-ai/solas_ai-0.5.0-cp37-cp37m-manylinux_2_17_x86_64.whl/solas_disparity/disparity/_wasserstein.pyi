import pandas as pd
from solas_disparity import const as const
from solas_disparity.types import Disparity as Disparity, DisparityCalculation as DisparityCalculation
from solas_disparity.utils import pgrg_ordered as pgrg_ordered
from typing import List, Optional

def wasserstein(group_data: pd.DataFrame, protected_groups: List[str], reference_groups: List[str], group_categories: List[str], outcome: pd.Series, label: Optional[pd.Series] = ..., sample_weight: Optional[pd.Series] = ..., lower_score_favorable: bool = ...) -> Disparity: ...
