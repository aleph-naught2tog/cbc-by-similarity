import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def render_clusters(
    cluster_count: int, labels: list[str], all_bird_series: list[pd.DataFrame]
):
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
                    all_bird_series[i], c="gray", alpha=0.4
                )
                cluster.append(all_bird_series[i])

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


def render_cluster_counts(cluster_count: int, labels: list[str]):
    cluster_c = [len(labels[labels == i]) for i in range(cluster_count)]
    cluster_n = ["Cluster " + str(i) for i in range(cluster_count)]

    plt.figure(figsize=(15, 5))
    plt.title("Cluster Distribution for KMeans")
    plt.bar(cluster_n, cluster_c)

    plt.show()
