import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
import math

from tslearn.clustering import TimeSeriesKMeans

from transform_helpers import json_to_dataframes

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

def render_clusters(cluster_count, labels, input):
    plot_count = math.ceil(math.sqrt(cluster_count))

    fig, axs = plt.subplots(plot_count, plot_count, figsize=(50, 50))
    fig.suptitle("Clusters")

    row_i = 0
    column_j = 0

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

def render_cluster_counts(cluster_count, labels):
    cluster_c = [len(labels[labels==i]) for i in range(cluster_count)]
    cluster_n = ["Cluster "+str(i) for i in range(cluster_count)]
    plt.figure(figsize=(15,5))
    plt.title("Cluster Distribution for KMeans")
    plt.bar(cluster_n,cluster_c)
    plt.show()

def timeserieskmeans_over_dataframes(input: list[pd.DataFrame]):

    # KMEANS https://www.kaggle.com/code/izzettunc/introduction-to-time-series-clustering?scriptVersionId=56314361&cellId=54

    # NOTE: this is honestly prob much higher than we need
    # elbows....
    cluster_count = math.ceil(math.sqrt(len(input)))

    tskmeans = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    # OKAY -- the dimension error was that all the series weren't the same length
    # happily I could fix that manually
    labels = tskmeans.fit_predict(input)

    ## graph clusters
    # render_clusters(labels=labels, cluster_count=cluster_count, input=input)

    # render_cluster_counts(cluster_count, labels)

def main():
    input_filename = "data/raw/bird_map_as_json.json"

    (all_bird_series, _bird_names) = json_to_dataframes(input_filename)

    timeserieskmeans_over_dataframes(input=all_bird_series)


if __name__ == "__main__":
    main()
