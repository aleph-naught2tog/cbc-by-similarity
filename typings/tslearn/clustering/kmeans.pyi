from typing import Literal, NewType, NotRequired, Sequence, TypedDict, Unpack

from pandas import DataFrame

# NOTE: this is a handmade file using JUST the things needed and JUST the overloads/types needed for the code. This is extremely NOT exhaustive.

# n_ts is the number of time series in the dataset
# sz is the length (number of timestamps) of the time series
# d is the dimensionality (number of modalities) of the time series

# added: mrc
TimeSeriesDataSet = NewType("TimeSeriesDataSet", tuple[int, int, int])

# added: mrc
class __DefTSKMInitKwargs(TypedDict):
    n_clusters: NotRequired[int]
    metric: NotRequired[
        Literal["dtw"] | Literal["softdtw"] | Literal["dtw"]
    ]

class TimeSeriesKMeans:
    inertia_: float
    n_iter_: int
    def __init__(self, **kwargs: Unpack[__DefTSKMInitKwargs]) -> None: ...
    def fit(self, X: Sequence[TimeSeriesDataSet] | list[DataFrame]) -> None: ...
    def fit_predict(self, X: Sequence[TimeSeriesDataSet]) -> Sequence[TimeSeriesDataSet]: ...
