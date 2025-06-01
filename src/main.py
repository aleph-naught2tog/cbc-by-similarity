import math
import pandas as pd
import os
import warnings
import matplotlib.pyplot as plt

from plotters import render_bird_graphs, render_cluster_counts, render_clusters, render_elbows
from transform_helpers import json_to_dataframes
from tslearn.clustering import TimeSeriesKMeans


# this silences all the sklearn future warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def timeserieskmeans_over_dataframes(
    all_bird_series: list[pd.DataFrame],
    dataframe_titles: list[str],
    cluster_count: int | None = None,
) -> None:

    render_bird_graphs(all_bird_series, bird_names=dataframe_titles)

    cluster_count = cluster_count or int(math.sqrt(len(all_bird_series)))

    render_elbows(all_bird_series, max_cluster_count=cluster_count)

    tskmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")
    cluster_labels = tskmeans.fit_predict(all_bird_series)

    ## graph clusters
    render_clusters(
        cluster_labels=cluster_labels,
        cluster_count=cluster_count,
        all_bird_series=all_bird_series,
    )

    render_cluster_counts(cluster_count, cluster_labels)

    # labeled_cluster_df = (
    #     pd.DataFrame(
    #         zip(dataframe_titles, labels),
    #         columns=["Bird", "Cluster"],
    #     )
    #     .sort_values(by="Cluster")
    #     .set_index("Bird")
    # )

    # labeled_cluster_df.to_csv("birds_and_cluster_indices-byPartyHour.csv")

def get_filename(relative_filename: str) -> str:
    cwd_folder = os.path.dirname(os.path.realpath(__file__)).rstrip("src")

    filename_without_slash = relative_filename.lstrip('/')

    return f"{cwd_folder}/{filename_without_slash}"

def main() -> None:
    input_filename = get_filename("/data/raw/bird_map_as_json.json")

    (all_bird_series, bird_names) = json_to_dataframes(input_filename)

    timeserieskmeans_over_dataframes(
        all_bird_series=all_bird_series,
        dataframe_titles=bird_names,
    )


if __name__ == "__main__":
    main()


# TODO:
#   * vary over which facet
#   * vary over which metric (euclidean, dtw, soft-dtw)
