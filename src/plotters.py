from typing import Any, Literal, NotRequired, TypedDict, Unpack, cast
import matplotlib.pyplot as plt
from numpy.typing import NDArray
import pandas as pd
from tslearn.clustering.kmeans import TimeSeriesKMeans

from tslearn.barycenters import euclidean_barycenter


class __DefRenderElbowsKwargs(TypedDict):
    max_cluster_count: int
    metric: NotRequired[Literal["dtw", "softdtw"]]


def compute_inertias(
    series: list[pd.DataFrame], **kwargs: Unpack[__DefRenderElbowsKwargs]
) -> tuple[list[float], list[int]]:
    metric = kwargs.get("metric", None)
    max_cluster_count = kwargs["max_cluster_count"]

    metric_kwargs = {"metric": metric} if metric else {}

    # inertia = the spread/variation of data points around the mean
    #   for kmeans, this is that concept around the centroids of each cluster
    #   how well the kmeans did the clumping!
    inertias: list[float] = []

    # 20 is just a reasonable default
    cluster_counts = list(range(1, max_cluster_count))

    for k in cluster_counts:
        # NOTE: might be able to clean things up so that we save all the clusters and then just call predict on the set with the cluster count we want... we do it here over euclidean distance, which is 1000000x faster than dtw
        tskmeans = TimeSeriesKMeans(n_clusters=k, **metric_kwargs)  # type: ignore -- it's angry because it widens `metric` to a string

        # .fit = compute the actual clustering
        tskmeans.fit(series)

        # save the inertia for checking
        inertias.append(tskmeans.inertia_)

    return (inertias, cluster_counts)


def render_elbows(
    all_bird_series: list[pd.DataFrame],
    **kwargs: Unpack[__DefRenderElbowsKwargs],
) -> None:
    max_cluster_count = kwargs["max_cluster_count"]
    metric = kwargs.get("metric", None)
    metric_kwargs = {"metric": metric} if metric else {}
    """Calculates the elbows for our kmeans and renders them

    Args:
        all_bird_series (list[pd.DataFrame]):
            A list of DataFrame objects containing time series information
    """

    (inertias, cluster_counts) = compute_inertias(
        all_bird_series,
        max_cluster_count=max_cluster_count,
        **metric_kwargs,  # type: ignore -- it's angry because it widens `metric` to a string
    )


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


def render_clusters_with_barycenters(
    cluster_labels: list[int],
    all_bird_series: list[pd.DataFrame],
) -> None:
    """Given the dataset, loop over it and render each graph within its cluster

    Args:
        cluster_count (int): How many clusters to make
        labels (list[int]): The list of labels from `fit_predict`
        all_bird_series (list[pd.DataFrame]):
            A list of DataFrame objects containing time series information
    """

    birds_with_clusters = list(zip(all_bird_series, cluster_labels))

    possible_labels = set(cluster_labels)

    for current_label in possible_labels:
        corresponding_bird_data = [
            datum
            for (datum, cluster_label) in birds_with_clusters
            if cluster_label == current_label
        ]

        ax1 = plt.subplot(4, 1, 1)
        plt.title("Euclidean barycenter")
        barycenter = euclidean_barycenter(corresponding_bird_data)

        # plot all points of the data set
        for series in corresponding_bird_data:
            plt.plot(series.to_numpy().ravel(), "k-", alpha=0.2)

        # plot the given barycenter of them
        plt.plot(barycenter.ravel(), "r-", linewidth=2)

        ax1.set_xlim([0, 91])

        # show the plot(s)
        # plt.tight_layout()
        plt.show()


def render_cluster_counts(cluster_count: int, labels: list[int]) -> None:
    """Render the distribution of the clusters

    Args:
        cluster_count (int): how many clusters exist
        labels (list[int]): the labels of each cluster
    """
    cluster_bar_heights = [
        len(labels[labels == i])  # type: ignore
        for i in range(cluster_count)
    ]

    cluster_bar_labels = ["Cluster " + str(i) for i in range(cluster_count)]

    plt.figure(figsize=(6, 6))
    plt.title("Cluster Distribution for KMeans")
    plt.bar(cluster_bar_labels, cluster_bar_heights)

    plt.show()
