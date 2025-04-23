from enum import Enum

class FeatureSet(str, Enum):
    DEFAULT = 'default'
    ALL = 'all'
    DISPARITY = 'disparity'
    FEATURE_SELECTION = 'feature_selection'
    HYPERPARAMETER_TUNING = 'hyperparameter_tuning'
    COMMERCIAL_BASE = 'commercial_base'
