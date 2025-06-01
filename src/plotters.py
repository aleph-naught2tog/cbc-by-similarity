
import math
from typing import Any, cast
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from tslearn.clustering.kmeans import TimeSeriesKMeans


def render_elbows(all_bird_series: list[pd.DataFrame]) -> None:
    """Calculates the elbows for our kmeans and renders them

    Args:
        all_bird_series (list[pd.DataFrame]):
            A list of DataFrame objects containing time series information
    """
    # inertia = the spread/variation of data points around the mean
    #   for kmeans, this is that concept around the centroids of each cluster
    #   how well the kmeans did the clumping!
    inertias: list[float] = []

    # 20 is just a reasonable default
    cluster_counts = list(range(1, 20))

    for k in cluster_counts:
        tskmeans = TimeSeriesKMeans(n_clusters=k)

        # .fit = compute the actual clustering
        tskmeans.fit(all_bird_series)
        print(tskmeans.n_iter_)

        # save the inertia for checking
        inertias.append(tskmeans.inertia_)

    print(inertias)

    # Plot sse against k
    figsize_num = math.floor(math.sqrt(len(all_bird_series)))
    figsize = (figsize_num, figsize_num)
    plt.figure(figsize=figsize)

    plt.plot(cluster_counts, inertias)

    # label the axes
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia")


def render_bird_graphs(
    all_bird_series: list[pd.DataFrame], bird_names: list[str]
) -> None:
    """Renders each CBC bird graph datum

    Args:
        all_bird_series (list[pd.DataFrame]):
            A list of DataFrame objects containing time series information
        bird_names (list[str]): The list of bird names_
    """
    how_many_tall = 20
    how_many_wide = 10

    _fig, untypedAxs = plt.subplots(how_many_tall, how_many_wide, figsize=(50, 50))

    axs = cast(NDArray[Any], untypedAxs)

    for row_i in range(how_many_tall):
        for column_j in range(how_many_wide):
            if row_i * how_many_wide + column_j + 1 > len(all_bird_series):
                continue

            ax = axs[row_i, column_j]
            di = row_i * how_many_wide + column_j
            datum = all_bird_series[di]
            print(datum)

            # `DataFrame.to_numpy is preferred` <- this just doesn't work
            ax.plot(datum.values) # type: ignore
            ax.set_title(bird_names[di])

    plt.show()


def render_clusters(
    cluster_count: int, labels: list[int], all_bird_series: list[pd.DataFrame]
) -> None:
    """Given the dataset, loop over it and render each graph within its cluster

    Args:
        cluster_count (int): How many clusters to make
        labels (list[int]): The list of labels from `fit_predict`
        all_bird_series (list[pd.DataFrame]):
            A list of DataFrame objects containing time series information
    """
    plot_count = math.ceil(math.sqrt(cluster_count))

    fig, bareAxs = plt.subplots(plot_count, plot_count, figsize=(50, 50))
    axs = cast(NDArray[Any], bareAxs)
    fig.suptitle("Clusters")

    row_i = 0
    column_j = 0

    for label in set(labels):
        cluster: list[pd.DataFrame] = []
        ax = axs[row_i, column_j]

        for i in range(len(labels)):
            if labels[i] == label:
                ax.plot(
                    all_bird_series[i], c="gray", alpha=0.4
                )

                cluster.append(all_bird_series[i])

        if len(cluster) > 0:
            ax.plot(
                np.average(np.vstack(cluster), axis=0), c="red"
            )

        ax.set_title("Cluster " + str(row_i * 10 + column_j))

        column_j += 1

        if column_j % plot_count == 0:
            row_i += 1
            column_j = 0

    plt.show()


def render_cluster_counts(cluster_count: int, labels: list[int]) -> None:
    """Render the distribution of the clusters

    Args:
        cluster_count (int): how many clusters exist
        labels (list[int]): the labels of each cluster
    """
    cluster_bar_heights = [
        # QUESTION: how and why does this work
        len(labels[labels == i])  # type: ignore
        for i in range(cluster_count)
    ]

    cluster_bar_labels = ["Cluster " + str(i) for i in range(cluster_count)]

    plt.figure(figsize=(15, 5))
    plt.title("Cluster Distribution for KMeans")
    plt.bar(cluster_bar_labels, cluster_bar_heights)

    plt.show()
