import json
import numpy as np
from scipy.spatial.distance import directed_hausdorff, cosine

from BirdData import BirdData

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.directed_hausdorff.html
# array


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


def calculate_counts_hausdorff(bird_data: BirdData, comparison_bird_name: str):
    bird_np = np.array(
        [
            (int(year), to_float_with_default(count))
            for (year, count) in bird_data.get_counts_by_bird(
                comparison_bird_name
            )
        ]
    )

    hausdorff_distances: list[tuple[str, tuple[float, float, float]]] = []

    for bird_name in bird_data.bird_names:
        counts = bird_data.get_counts_by_bird(bird_name)
        np_counts = np.array(
            [
                (int(year), to_float_with_default(count))
                for (year, count) in counts
            ]
        )

        hausdorff_distances.append(
            (bird_name, directed_hausdorff(bird_np, np_counts))
        )

    sorted_by_hd = sorted(hausdorff_distances, key=lambda d: d[1])

    return sorted_by_hd


# # BUG: this won't work until we normalize over the years, which just isn't working rn
# def calculate_cosine_similarities(
#     bird_data: BirdData, comparison_bird_name: str
# ):
#     bird_list = [
#         to_float_with_default(count)
#         for (_year, count) in bird_data.get_counts_by_bird(comparison_bird_name)
#     ]
#     bird_np = np.array(bird_list)

#     cosine_similarities: list[tuple[str, float]] = []

#     for bird_name in bird_data.bird_names:
#         print(f"{bird_name.upper()}")
#         counts = bird_data.get_counts_by_bird(bird_name)

#         count_list = [to_float_with_default(count) for (_year, count) in counts]
#         np_counts = np.array(count_list)

#         cosine_similarities.append((bird_name, 1 - cosine(bird_np, np_counts)))


#     sorted_by_cos = sorted(cosine_similarities, key=lambda d: d[1])

#     return sorted_by_cos


def main():
    input_filename = "data/raw/bird_map_as_json.json"

    bird_data = translate_json_to_bird_data(input_filename)

    # for bird_name, (hd, _i, _j) in calculate_counts_hausdorff(
    #     bird_data, "Greater White-fronted Goose"
    # ):
        # print(f"{bird_name}: {hd}")

    print("---------------------------------------------")
    print("---------------------------------------------")
    print("---------------------------------------------")

    for bird_name, cos in calculate_cosine_similarities(
        bird_data, "Greater White-fronted Goose"
    ):
        print(f"{bird_name}: {cos}")


if __name__ == "__main__":
    main()
