import numpy as np

import pandas as pd

import matplotlib.pyplot as plt
import math

from sklearn.cluster import KMeans

from BirdData import BirdData
from transform_helpers import to_float_with_default
from tslearn.clustering import TimeSeriesKMeans
from sklearn.cluster import KMeans

# next: https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py


def kmeans_test_run(bird_data: BirdData):
    bird_list = [
        (year, to_float_with_default(count))
        for (year, count) in bird_data.get_by_bird("House Sparrow", "howMany")
    ]

    x = list(list(zip(*bird_list)))[0]
    y = list(list(zip(*bird_list)))[1]

    # plt.scatter(x, y)
    # plt.show()

    data = np.array(bird_list)
    inertias = []

    # the max number of clusters is 1 per point
    cluster_range = range(1, len(bird_list) + 1)

    # this gives us an "elbow" to show which cluster count is good
    for i in cluster_range:
        print(".", end="")
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    # plt.plot(cluster_range, inertias, marker="o")
    # plt.title("Elbow method")
    # plt.xlabel("Number of clusters")
    # plt.ylabel("Inertia")
    # plt.show()

    # 2
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(data)

    plt.scatter(x, y, c=kmeans.labels_)
    plt.show()


def fake_kmeans_pd() -> None:
    all_series = []

    csv1 = [[1800, 0], [1900, 5], [2000, 25]]
    csv2 = [[1800, 10], [1900, 7], [2000, 40]]
    csv3 = [[1800, 0], [1900, 4], [2000, 20]]

    csvs = [csv1, csv2, csv3]

    for current_csv in csvs:
        df = pd.DataFrame(current_csv, columns=["year", "value"])
        all_series.append(df)

    print(all_series[0])
    print(len(all_series))

    # how_many_tall = 2
    # how_many_wide = 3

    # # right now, this is plotting BOTH values in the graph
    # # so we end up with a line for the time
    # for i in range(how_many_tall):
    #     for j in range(how_many_wide):
    #         index_in_plots = i * how_many_wide + j
    #         if index_in_plots + 1 > len(all_series):
    #             continue

    #         datum = all_series[index_in_plots]
    #         print(datum)

    # axs[i, j].plot(datum)
    # datum.plot(x='year')

    # plt.show()
    # A good rule of thumb is choosing k as the square root of the number of points in the training data set in kNN

    cluster_count = math.ceil(math.sqrt(len(all_series)))

    plot_count = math.ceil(math.sqrt(cluster_count))

    km = TimeSeriesKMeans(n_clusters=cluster_count, metric="dtw")

    labels = km.fit_predict(all_series)

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
                axs[row_i, column_j].plot(all_series[i], c="gray", alpha=0.4)
                cluster.append(all_series[i])

        if len(cluster) > 0:
            axs[row_i, column_j].plot(
                np.average(np.vstack(cluster), axis=0), c="red"
            )

        column_j += 1

        if column_j % plot_count == 0:
            row_i += 1
            column_j = 0

    plt.show()


def bare_kmeans(bird_data: BirdData) -> None:
    timeseries_list: list[list[tuple[int, float]]] = []
    how = "numberByPartyHours"

    for bird_name in bird_data.bird_names:
        timeseries = [
            (int(year), to_float_with_default(count))
            for (year, count) in bird_data.get_by_bird(bird_name, how)
        ]

        timeseries_list.append(timeseries)

    # NOTE: dimension issues
    data = pd.DataFrame(timeseries_list)

    how_many_tall = 20
    how_many_wide = 10
    fig, axs = plt.subplots(how_many_tall, how_many_wide, figsize=(50, 50))

    for i in range(how_many_tall):
        for j in range(how_many_wide):
            if i * how_many_wide + j + 1 > len(data):
                continue

            di = i * how_many_wide + j
            datum = data[di]

            axs[i, j].plot(list(zip(*datum.values))[0])

    plt.show()


def main():
    input_filename = "data/raw/bird_map_as_json.json"

    # bird_data = translate_json_to_bird_data(input_filename)

    fake_kmeans_pd()

    # bird = "Red-winged Blackbird"
    # kmeans_test_run(bird_data)
    # bare_kmeans(bird_data)

    # write_cosine_similarities_file(bird_data=bird_data, how="howMany")
    # write_cosine_similarities_file(
    #     bird_data=bird_data, how="numberByPartyHours"
    # )

    # write_hausdorff_distances_file(bird_data=bird_data, how="howMany")
    # write_hausdorff_distances_file(
    #     bird_data=bird_data, how="numberByPartyHours"
    # )


if __name__ == "__main__":
    main()
