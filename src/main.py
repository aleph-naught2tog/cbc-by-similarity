import json
import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
import math

from tslearn.clustering import TimeSeriesKMeans

# next: https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py


# https://tslearn.readthedocs.io/en/stable/auto_examples/clustering/plot_kmeans.html#sphx-glr-auto-examples-clustering-plot-kmeans-py


def render_bird_graphs(all_bird_series: list[pd.DataFrame]):
    how_many_tall = 20
    how_many_wide = 10
    _fig, axs = plt.subplots(how_many_tall, how_many_wide, figsize=(50, 50))

    for i in range(how_many_tall):
        for j in range(how_many_wide):
            if i * how_many_wide + j + 1 > len(all_bird_series):
                continue

            di = i * how_many_wide + j
            datum = all_bird_series[di]
            print(datum)

            axs[i, j].plot(datum.values)
            axs[i, j].set_title(bird_names[di])

    plt.show()


# NOTE: we are coercing None to -1
def json_to_dataframes(
    json_filename: str,
) -> tuple[list[pd.DataFrame], list[str]]:
    all_bird_series: list[pd.DataFrame] = []
    bird_names: list[str] = []

    with open(json_filename) as j:
        d = json.load(j)

        # out: {  bird_name: bird_name, x_years: [...years], y_how_many: [...howMany], y_by_party_hours: [...partyHours]}
        for bird_name, itemsByYear in d.items():
            byYearItems = itemsByYear.items()
            bird_dict = {
                # "bird_name": bird_name,
                "x_years": [year for (year, _datum) in byYearItems],
                "y_how_many": [
                    (-1 if datum["howMany"] is None else datum["howMany"])
                    for (_year, datum) in byYearItems
                ],
                # "y_by_party_hours": [
                #     datum["numberByPartyHours"]
                #     for (_year, datum) in byYearItems
                # ],
            }

            bird_df = pd.DataFrame(bird_dict)
            bird_df.loc[:, ["x_years", "y_how_many"]]
            bird_df.set_index("x_years", inplace=True)

            all_bird_series.append(bird_df)
            bird_names.append(bird_name)

    return (all_bird_series, bird_names)

def normalize_series_lengths(mySeries):
    series_lengths = {len(series) for series in mySeries}
    print(series_lengths)

    ind = 0
    for series in mySeries:
        print("["+str(ind)+"] "+series.index[0]+" "+series.index[len(series)-1])
        ind+=1


def timeserieskmeans_over_dataframes(input: list[pd.DataFrame]):
    normalize_series_lengths(input)

    # KMEANS https://www.kaggle.com/code/izzettunc/introduction-to-time-series-clustering?scriptVersionId=56314361&cellId=54

    cluster_count = math.ceil(math.sqrt(len(input)))
    kmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    # dimension error here
    # example says we need to use things as a single datum
    # and doesn't really say how
    # OKAY -- the dimension error was that all the series weren't the same length
    # happily I could fix that manually
    print(input)
    labels = kmeans.fit_predict(input)

    ## graph clusters
    plot_count = math.ceil(math.sqrt(cluster_count))

    fig, axs = plt.subplots(plot_count, plot_count, figsize=(25, 25))
    fig.suptitle("Clusters")

    row_i = 0
    column_j = 0
    # For each label there is,
    # plots every series with that label
    for label in set(labels):
        cluster = []
        for i in range(len(labels)):
            if labels[i] == label:
                axs[row_i, column_j].plot(
                    input[i], c="gray", alpha=0.4
                )
                cluster.append(input[i])

        if len(cluster) > 0:
            axs[row_i, column_j].plot(
                np.average(np.vstack(cluster), axis=0), c="red"
            )

        axs[row_i, column_j].set_title("Cluster " + str(row_i * 10 + column_j))

        column_j += 1

        if column_j % plot_count == 0:
            row_i += 1
            column_j = 0

    plt.show()

def main():
    input_filename = "data/raw/bird_map_as_json.json"

    (all_bird_series, _bird_names) = json_to_dataframes(input_filename)

    timeserieskmeans_over_dataframes(input=all_bird_series)


if __name__ == "__main__":
    main()
