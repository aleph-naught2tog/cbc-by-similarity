import getopt
import math
import numpy
import pandas as pd
import sys

# from plotters import render_bird_graphs, render_cluster_counts, render_clusters, render_elbows
from plotters import render_elbows
from transform_helpers import json_to_dataframes
from tslearn.clustering import TimeSeriesKMeans

def timeserieskmeans_over_dataframes(
    all_bird_series: list[pd.DataFrame],
    dataframe_titles: list[str],
    cluster_count: int | None,
) -> None:
    # NOTE: this is honestly prob much higher than we need
    # elbows....
    cluster_count = cluster_count or int(math.sqrt(len(all_bird_series)))

    render_elbows(all_bird_series)

    # OKAY -- the dimension error was that all the series weren't the same length
    # happily I could fix that manually
    _tskmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")
    # labels = tskmeans.fit_predict(all_bird_series)

    # render_bird_graphs(all_bird_series, bird_names=dataframe_titles)

    # ## graph clusters
    # render_clusters(
    #     labels=labels,
    #     cluster_count=cluster_count,
    #     all_bird_series=all_bird_series,
    # )

    # render_cluster_counts(cluster_count, labels)

    # labeled_cluster_df = (
    #     pd.DataFrame(
    #         zip(dataframe_titles, labels),
    #         columns=["Bird", "Cluster"],
    #     )
    #     .sort_values(by="Cluster")
    #     .set_index("Bird")
    # )

    # labeled_cluster_df.to_csv("birds_and_cluster_indices-byPartyHour.csv")


def get_cluster_count() -> int | None:
    options = "c:"
    long_options = ["cluster-count="]

    argumentsAndValues = getopt.getopt(sys.argv[1:], options, long_options)
    arg_cluster_count = argumentsAndValues[0]

    cluster_count = int(arg_cluster_count[0][1]) if arg_cluster_count else None

    return cluster_count


def main() -> None:
    number_of_clusters = get_cluster_count()

    input_filename = "data/raw/bird_map_as_json.json"

    (all_bird_series, bird_names) = json_to_dataframes(input_filename)

    timeserieskmeans_over_dataframes(
        all_bird_series=all_bird_series,
        dataframe_titles=bird_names,
        cluster_count=number_of_clusters,
    )


if __name__ == "__main__":
    main()
