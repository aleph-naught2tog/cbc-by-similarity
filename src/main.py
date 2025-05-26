import csv
import json
import numpy as np
from scipy.spatial.distance import cosine, directed_hausdorff
from typing import Any, Literal, Sequence

import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

from BirdData import BirdData

# next: https://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py

def translate_json_to_bird_data(input_filename: str) -> BirdData:
    raw_json = {}

    with open(input_filename, newline="") as f:
        raw_json = json.load(f)

    bird_data = BirdData(raw_json)

    return bird_data


def to_float_with_default(val: float | None) -> float:
    if val is None:
        return -1
    else:
        return val


def calculate_hausdorff_distance(
    data: BirdData,
    comparison_bird_name: str,
    how: Literal["howMany"] | Literal["numberByPartyHours"],
):
    bird_np = np.array(
        [
            (int(year), to_float_with_default(count))
            for (year, count) in data.get_by_bird(comparison_bird_name, how)
        ]
    )

    hausdorff_distances: list[tuple[str, float]] = []

    for bird_name in data.bird_names:
        counts = data.get_by_bird(bird_name, how)
        count_list = [
            (int(year), to_float_with_default(count))
            for (year, count) in counts
        ]

        np_counts = np.array(count_list)

        hausdorff_distances.append(
            (bird_name, directed_hausdorff(bird_np, np_counts)[0])
        )

    return hausdorff_distances


def calculate_cosine_similarities(
    data: BirdData,
    comparison_bird_name: str,
    how: Literal["howMany"] | Literal["numberByPartyHours"],
):
    bird_list = [
        to_float_with_default(count)
        for (_year, count) in data.get_by_bird(comparison_bird_name, how)
    ]

    bird_np = np.array(bird_list)

    cosine_similarities: list[tuple[str, float]] = []

    for bird_name in data.bird_names:
        counts = data.get_by_bird(bird_name, how)

        # NOTE: we divide by 10 here to avoid scalar overflow
        count_list = [
            (to_float_with_default(count) / 100) for (_year, count) in counts
        ]
        np_counts = np.array(count_list)

        cosine_similarities.append((bird_name, 1 - cosine(bird_np, np_counts)))

    return cosine_similarities


def write_to_tsv(csv_lines: Sequence[Sequence[Any]], output_filename: str):
    with open(output_filename, "w", newline="") as tsv:
        writer = csv.writer(tsv, delimiter="\t", quoting=csv.QUOTE_STRINGS)
        writer.writerows(csv_lines)


def get_filename(
    how: str,
    method: str,
):
    filename_base = "data/processed"
    core_filename = "cbc-bird-comparisons"
    ext = "tsv"

    return f"{filename_base}/{core_filename}_{how}_{method}.{ext}"


def write_cosine_similarities_file(
    bird_data: BirdData, how: Literal["howMany"] | Literal["numberByPartyHours"]
):
    header = ["bird_name"] + bird_data.bird_names
    csv_lines: list[Sequence[float | str]] = [header]

    for bird_name in bird_data.bird_names:
        results = calculate_cosine_similarities(
            data=bird_data,
            comparison_bird_name=bird_name,
            how=how,
        )

        cs_vals: list[float] = list(list(zip(*results))[1])
        cs = [float(format(val, ".5f")) for val in cs_vals]

        row = [bird_name] + cs

        csv_lines.append(row)

    output_filename = get_filename(how + "-over-100", method="cosine")
    write_to_tsv(csv_lines=csv_lines, output_filename=output_filename)


def write_hausdorff_distances_file(
    bird_data: BirdData, how: Literal["howMany"] | Literal["numberByPartyHours"]
):
    header = ["bird_name"] + bird_data.bird_names
    csv_lines: list[Sequence[float | str]] = [header]

    for bird_name in bird_data.bird_names:
        results = calculate_hausdorff_distance(
            data=bird_data,
            comparison_bird_name=bird_name,
            how=how,
        )

        cs_vals: list[float] = list(list(zip(*results))[1])
        cs = [float(format(val, ".5f")) for val in cs_vals]

        row = [bird_name] + cs

        csv_lines.append(row)

    output_filename = get_filename(how, method="hausdorff")
    write_to_tsv(csv_lines=csv_lines, output_filename=output_filename)


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


def cosine_kmeans(bird_data: BirdData):
    x_indices = range(0, len(bird_data.bird_names))
    results_by_bird_index: list[list[float]] = []
    house_sparrow_index = bird_data.bird_names.index("Northern Cardinal")

    # get the values
    for bird_name in bird_data.bird_names:
        results = calculate_cosine_similarities(
            data=bird_data,
            comparison_bird_name=bird_name,
            how="numberByPartyHours",
        )

        vals: list[float] = list(list(zip(*results))[1])
        results_by_bird_index.append(vals)

    house_sparrow_data = results_by_bird_index[house_sparrow_index]

    x = x_indices
    y = house_sparrow_data

    data = np.array(list(zip(x, y)))
    inertias = []

    # the max number of clusters is 1 per point
    # we cap it at 25 because that is easier to read and the elbow is way ahead of that
    cluster_range = range(1, 25)

    # this gives us an "elbow" to show which cluster count is good
    for i in cluster_range:
        print(".", end="")
        kmeans = KMeans(n_clusters=i,init="random")
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    # plot the cluster count options
    plt.plot(cluster_range, inertias, marker="o")
    plt.title("Elbow method")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.show()

    cluster_count = 4
    kmeans = KMeans(n_clusters=cluster_count)
    kmeans.fit(data)

    # plot the bird indexes + cosine similarities
    plt.scatter(x, y, c=kmeans.labels_)
    plt.show()

def hausdorff_kmeans(bird_data: BirdData):
    x_indices = range(0, len(bird_data.bird_names))
    results_by_bird_index: list[list[float]] = []
    house_sparrow_index = bird_data.bird_names.index("Northern Cardinal")

    # get the values
    for bird_name in bird_data.bird_names:
        results = calculate_hausdorff_distance(
            data=bird_data,
            comparison_bird_name=bird_name,
            # NOTE: this is where you change which key you're using
            how="numberByPartyHours",
        )

        vals: list[float] = list(list(zip(*results))[1])
        results_by_bird_index.append(vals)

    house_sparrow_data = results_by_bird_index[house_sparrow_index]

    x = x_indices
    y = house_sparrow_data

    data = np.array(list(zip(x, y)))
    inertias = []

    # the max number of clusters is 1 per point
    # we cap it at 25 because that is easier to read and the elbow is way ahead of that
    cluster_range = range(1, 25)

    # this gives us an "elbow" to show which cluster count is good
    for i in cluster_range:
        print(".", end="")
        kmeans = KMeans(n_clusters=i,init="random")
        kmeans.fit(data)
        inertias.append(kmeans.inertia_)

    # plot the cluster count options
    plt.plot(cluster_range, inertias, marker="o")
    plt.title("Elbow method")
    plt.xlabel("Number of clusters")
    plt.ylabel("Inertia")
    plt.show()

    cluster_count = 4
    kmeans = KMeans(n_clusters=cluster_count)
    kmeans.fit(data)

    # plot the bird indexes + cosine similarities
    plt.scatter(x, y, c=kmeans.labels_)
    plt.show()


def main():
    input_filename = "data/raw/bird_map_as_json.json"

    bird_data = translate_json_to_bird_data(input_filename)

    # kmeans_test_run(bird_data)
    cosine_kmeans(bird_data=bird_data)

    print("-------------- next is hausdorff")

    hausdorff_kmeans(bird_data=bird_data)

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
