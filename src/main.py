import getopt
import math
import pandas as pd
import sys

from transform_helpers import json_to_dataframes
from tslearn.clustering import TimeSeriesKMeans


def timeserieskmeans_over_dataframes(
    input: list[pd.DataFrame],
    dataframe_titles: list[str],
    cluster_count: int | None,
):
    # NOTE: this is honestly prob much higher than we need
    # elbows....
    cluster_count = cluster_count or int(math.sqrt(len(input)))

    tskmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    # OKAY -- the dimension error was that all the series weren't the same length
    # happily I could fix that manually
    labels = tskmeans.fit_predict(input)

    ## graph clusters
    # render_clusters(labels=labels, cluster_count=cluster_count, input=input)

    # render_cluster_counts(cluster_count, labels)

    fancy_names_for_labels = [f"Cluster {label}" for label in labels]

    labeled_cluster_df = (
        pd.DataFrame(
            zip(dataframe_titles, fancy_names_for_labels),
            columns=["Series", "Cluster"],
        )
        .sort_values(by="Cluster")
        .set_index("Series")
    )

    print(labeled_cluster_df)


def get_cluster_count() -> int | None:
    options = "c:"
    long_options = ["cluster-count="]

    argumentsAndValues = getopt.getopt(sys.argv[1:], options, long_options)
    arg_cluster_count = argumentsAndValues[0]

    cluster_count = int(arg_cluster_count[0][1]) if arg_cluster_count else None

    return cluster_count


def main():
    number_of_clusters = get_cluster_count()

    input_filename = "data/raw/bird_map_as_json.json"

    (all_bird_series, bird_names) = json_to_dataframes(input_filename)

    timeserieskmeans_over_dataframes(
        input=all_bird_series,
        dataframe_titles=bird_names,
        cluster_count=number_of_clusters,
    )


if __name__ == "__main__":
    main()
