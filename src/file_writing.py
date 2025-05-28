import csv

from typing import Any, Literal, Sequence

from BirdData import BirdData
from calculations import (
    calculate_cosine_similarities,
    calculate_hausdorff_distance,
)


def write_to_tsv(
    csv_lines: Sequence[Sequence[Any]], output_filename: str
) -> None:
    with open(output_filename, "w", newline="") as tsv:
        writer = csv.writer(tsv, delimiter="\t", quoting=csv.QUOTE_STRINGS)
        writer.writerows(csv_lines)


def get_filename(
    how: str,
    method: str,
) -> str:
    filename_base = "data/processed"
    core_filename = "cbc-bird-comparisons"
    ext = "tsv"

    return f"{filename_base}/{core_filename}_{how}_{method}.{ext}"


def write_cosine_similarities_file(
    bird_data: BirdData, how: Literal["howMany"] | Literal["numberByPartyHours"]
) -> None:
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
) -> None:
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
