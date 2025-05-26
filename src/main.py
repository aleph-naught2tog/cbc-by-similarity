import csv
import numpy as np

from typing import Any, Literal, Sequence

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

from BirdData import BirdData
from transform_helpers import to_float_with_default, translate_json_to_bird_data

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

def bare_kmeans(bird_data: BirdData):


def main():
    input_filename = "data/raw/bird_map_as_json.json"

    bird_data = translate_json_to_bird_data(input_filename)

    bird = "Red-winged Blackbird"
    # kmeans_test_run(bird_data)

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
