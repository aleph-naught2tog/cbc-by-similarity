import math
from matplotlib import pyplot as plt
import pandas as pd
import os
import warnings

from sklearn.metrics import silhouette_score

from typing import Literal

from app_types import HowT
from plotters import (
    render_bird_graphs,
    render_cluster_counts,
    render_clusters_with_barycenters,
    render_elbows,
)
from tslearn.utils import to_time_series_dataset
from transform_helpers import bar_chart_to_dataframes, cbc_json_to_dataframes
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from itertools import product


# this silences all the sklearn future warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def timeserieskmeans_over_dataframes(
    all_bird_series: list[pd.DataFrame],
    dataframe_titles: list[str],
    cluster_count: int | None = None,
) -> None:
    seed = 0
    # render_bird_graphs(all_bird_series, bird_names=dataframe_titles)

    final_cluster_count = cluster_count or int(math.sqrt(len(all_bird_series)))

    # render_elbows(all_bird_series, seed=0, max_cluster_count=final_cluster_count)

    tskmeans = TimeSeriesKMeans(
        n_clusters=final_cluster_count, metric="dtw", random_state=seed
    )
    cluster_labels: list[int] = tskmeans.fit_predict(all_bird_series)  # type: ignore because it wants a different shape, but this works

    ## graph clusters
    render_clusters_with_barycenters(
        cluster_labels=cluster_labels,
        all_bird_series=all_bird_series,
    )

    render_cluster_counts(final_cluster_count, cluster_labels)


def write_dataframes_and_cluster_index_to_file(
    dataframe_titles: list[str],
    labels: list[int],
    how: HowT,
    method: Literal["hotspot"] | Literal["cbc"],
) -> None:
    labeled_cluster_df = (
        pd.DataFrame(
            zip(dataframe_titles, labels),
            columns=["Bird", "Cluster"],
        )
        .sort_values(by="Cluster")
        .set_index("Bird")
    )

    f = f"/data/processed/bci_{method}-{how}.csv"
    labeled_cluster_df.to_csv(get_filename(f))


# I... don't know if I can move this function and have it still work correctly?
def get_filename(relative_filename: str) -> str:
    cwd_folder = os.path.dirname(os.path.realpath(__file__)).rstrip("src")

    filename_without_slash = relative_filename.lstrip("/")

    return f"{cwd_folder}/{filename_without_slash}"


def main() -> None:
    input_filename = get_filename(
        "/data/raw/hotspot/ebird_L199454__1980_2025_1_12_barchart.txt"
    )
    (all_bird_series, bird_names) = bar_chart_to_dataframes(input_filename)

    # input_filename = get_filename("/data/raw/cbc/bird_map_as_json.json")

    # (all_bird_series, bird_names) = cbc_json_to_dataframes(input_filename)

    timeserieskmeans_over_dataframes(
        all_bird_series=all_bird_series,
        dataframe_titles=bird_names,
    )


if __name__ == "__main__":
    main()
