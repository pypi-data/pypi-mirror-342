from enum import Enum

class FeatureSet(str, Enum):
    DEFAULT: str
    ALL: str
    DISPARITY: str
    FEATURE_SELECTION: str
    HYPERPARAMETER_TUNING: str
    COMMERCIAL_BASE: str
