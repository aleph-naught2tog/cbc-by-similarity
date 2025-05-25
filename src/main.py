import csv
import json
import numpy as np
from scipy.spatial.distance import cosine
from typing import Any, Literal

from BirdData import BirdData


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


def calculate_cosine_similarities(
    bird_data: BirdData,
    comparison_bird_name: str,
    how: Literal["howMany"] | Literal["numberByPartyHours"],
):
    bird_list = [
        to_float_with_default(count)
        for (_year, count) in bird_data.get_by_bird(comparison_bird_name, how)
    ]

    bird_np = np.array(bird_list)

    cosine_similarities: list[tuple[str, float]] = []

    for bird_name in bird_data.bird_names:
        counts = bird_data.get_by_bird(bird_name, how)

        count_list = [to_float_with_default(count) for (_year, count) in counts]
        np_counts = np.array(count_list)

        cosine_similarities.append((bird_name, 1 - cosine(bird_np, np_counts)))

    return cosine_similarities


def write_to_tsv(csv_lines: list[list[Any]], output_filename: str):
    with open(output_filename, "w", newline="") as tsv:
        writer = csv.writer(tsv, delimiter="\t", quoting=csv.QUOTE_STRINGS)
        writer.writerows(csv_lines)


def main():
    input_filename = "data/raw/bird_map_as_json.json"
    output_filename = "data/processed/birds_with_comparisons.tsv"

    bird_data = translate_json_to_bird_data(input_filename)

    header = ["bird_name"] + bird_data.bird_names
    csv_lines = [header]

    for compared_bird_name in bird_data.bird_names:
        cos_similarities = calculate_cosine_similarities(
            bird_data, compared_bird_name, how="numberByPartyHours"
        )

        cs_vals: list[float] = list(list(zip(*cos_similarities))[1])
        cs = [float(format(val, ".5f")) for val in cs_vals]

        row = [compared_bird_name] + cs

        csv_lines.append(row)

    write_to_tsv(csv_lines=csv_lines, output_filename=output_filename)


if __name__ == "__main__":
    main()
