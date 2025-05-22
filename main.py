import csv
import json
import os
from typing import Tuple, NewType, cast
import numpy as np

# in:  { [birdName]: { year: { howMany, numberByPartyHours }}}
# out: bird_name,year,how_many,number_by_party_hours
#      .....

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.directed_hausdorff.html
# array

BirdDataCSV = NewType(
    "BirdDataCSV",
    list[list[str] | Tuple[str, int, float | None, float | None]],
)


def translate_bird_map_json_to_csv(
    input_filename: str, output_filename: str
) -> None:
    if os.path.exists(output_filename):
        print("Output file exists; no need to recreate.")
        return

    csv_data: BirdDataCSV = cast(BirdDataCSV, [])
    header = ["bird_name", "year", "how_many", "number_by_party_hours"]

    csv_data.append(header)

    with open(input_filename, newline="") as f:
        loaded_json = json.load(f)
        for bird_name, results_by_year in loaded_json.items():
            for year, data in results_by_year.items():
                row = [
                    bird_name,
                    (year),
                    data["howMany"],
                    data["numberByPartyHours"],
                ]
                csv_data.append(row)

    with open(output_filename, "w", newline="") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_STRINGS)
        # I don't understand why the years are being quoted but that's fine
        writer.writerows(csv_data)


def main():
    input_filename = "data/raw/bird_map_as_json.json"
    output_filename = "data/processed/bird_map.csv"
    # I feel like there might be a more built-in way of doing this, or skipping the CSV write step completely, but fine for now
    translate_bird_map_json_to_csv(input_filename, output_filename)

    res = np.genfromtext(output_filename, delimiter=',')


if __name__ == "__main__":
    main()
