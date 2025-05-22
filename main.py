import json
import os
from typing import Tuple, NewType, cast

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
        return

    csv_data: BirdDataCSV = cast(BirdDataCSV, [])
    header = ["bird_name", "year", "how_many", "number_by_party_hours"]

    csv_data.append(header)

    with open(input_filename) as f:
        loaded_json = json.load(f)
        for bird_name, results_by_year in loaded_json.items():
            for year, data in results_by_year.items():
                row = [
                    bird_name,
                    year,
                    data["howMany"],
                    data["numberByPartyHours"],
                ]
                csv_data.append(row)

    write_bird_csv(csv_data=csv_data, filename=output_filename)


def write_bird_csv(
    csv_data: BirdDataCSV, filename: str = "data/processed/bird_map.csv"
) -> None:
    with open(filename, "w") as f:
        for row in csv_data:
            row_length = len(row)
            for index, value in enumerate(row):
                value_string = ""

                if type(value) is str:
                    value_string = f'"{value}"'
                elif type(value) is int or type(value) is float:
                    value_string = str(value)
                elif value is None:
                    value_string = ""
                else:
                    raise Exception(f"Unexpected type, {value}, {type(value)}")

                # only add trailing comma if it's not the last item
                if index < row_length - 1:
                    value_string += ','

                f.write(value_string)
            f.write('\n')


def main():
    input_filename = "data/raw/bird_map_as_json.json"
    output_filename = "data/processed/bird_map.csv"
    translate_bird_map_json_to_csv(
        input_filename=input_filename, output_filename=output_filename
    )


if __name__ == "__main__":
    main()
