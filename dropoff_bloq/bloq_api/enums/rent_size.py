from enum import Enum

class RentSize(str, Enum):
    XS = "extra_small"
    S = "small"
    M = "medium"
    L = "large"
    XL = "extra_large"