import math
from typing import Any, TypedDict, Unpack, cast
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from tslearn.clustering.kmeans import TimeSeriesKMeans

from tslearn.barycenters import dtw_barycenter_averaging, euclidean_barycenter


class __DefRenderElbowsKwargs(TypedDict):
    max_cluster_count: int

def render_elbows(
    all_bird_series: list[pd.DataFrame],
    **kwargs: Unpack[__DefRenderElbowsKwargs],
) -> None:
    max_cluster_count = kwargs["max_cluster_count"]

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
    cluster_counts = list(range(1, max_cluster_count))

    for k in cluster_counts:
        # NOTE: might be able to clean things up so that we save all the clusters and then just call predict on the set with the cluster count we want
        tskmeans = TimeSeriesKMeans(n_clusters=k)

        # .fit = compute the actual clustering
        tskmeans.fit(all_bird_series)

        # save the inertia for checking
        inertias.append(tskmeans.inertia_)

    # Plot sse against k
    figsize_num = 6
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

    _fig, untypedAxs = plt.subplots(
        how_many_tall, how_many_wide, figsize=(50, 50)
    )

    axs = cast(NDArray[Any], untypedAxs)

    for row_i in range(how_many_tall):
        for column_j in range(how_many_wide):
            if row_i * how_many_wide + column_j + 1 > len(all_bird_series):
                continue

            ax = axs[row_i, column_j]
            di = row_i * how_many_wide + column_j
            datum = all_bird_series[di]

            # `DataFrame.to_numpy is preferred` <- this just doesn't work
            ax.plot(datum.values)  # type: ignore
            ax.set_title(bird_names[di])

    plt.show()


def render_clusters(
    cluster_count: int, cluster_labels: list[int], all_bird_series: list[pd.DataFrame]
) -> None:
    """Given the dataset, loop over it and render each graph within its cluster

    Args:
        cluster_count (int): How many clusters to make
        labels (list[int]): The list of labels from `fit_predict`
        all_bird_series (list[pd.DataFrame]):
            A list of DataFrame objects containing time series information
    """
    plot_count = math.ceil(math.sqrt(cluster_count))


    d = list(zip(all_bird_series, cluster_labels))

    possible_labels = set(cluster_labels)

    graphs: list[list[pd.DataFrame]] = []

    for current_label in possible_labels:
        corresponding_bird_data = [
            datum
            for (datum, cluster_label) in d
            if cluster_label == current_label
        ]
        # graphs.append(corresponding_bird_data)

        X = corresponding_bird_data
        ax1 = plt.subplot(4, 1, 1)
        plt.title("Euclidean barycenter")
        barycenter = euclidean_barycenter(X)

        # plot all points of the data set
        for series in X:
            plt.plot(series.to_numpy().ravel(), "k-", alpha=.2)
        # plot the given barycenter of them
        plt.plot(barycenter.ravel(), "r-", linewidth=2)

        ax1.set_xlim([0, 91])

        # show the plot(s)
        plt.tight_layout()
        plt.show()




    # fig, bareAxs = plt.subplots(plot_count, plot_count, figsize=(10,10))
    # axs = cast(NDArray[Any], bareAxs)
    # fig.suptitle("Clusters")

    # row_i = 0
    # column_j = 0























    # # for each possible cluster label
    # for current_cluster_label in set(cluster_labels):
    #     clustered_graphs: list[pd.DataFrame] = []
    #     ax = axs[row_i, column_j]

    #     # for each index in the set of numbers from 1 to the last cluster label
    #     for i in range(len(cluster_labels)):
    #         cluster_label_in_range = cluster_labels[i]
    #         if cluster_label_in_range == current_cluster_label:
    #             ax.plot(all_bird_series[i], c="gray", alpha=0.4)

    #             clustered_graphs.append(all_bird_series[i])

    #     column_j += 1

    #     if column_j % plot_count == 0:
    #         row_i += 1
    #         column_j = 0

    # plt.tight_layout()
    # plt.show()


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

    plt.figure(figsize=(6, 6))
    plt.title("Cluster Distribution for KMeans")
    plt.bar(cluster_bar_labels, cluster_bar_heights)

    plt.show()
