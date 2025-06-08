import json
import pandas as pd
import csv

from app_types import HowT


def cbc_json_to_dataframes(
    json_filename: str,
    how: HowT = "how_many",
    noneValue: int | float = -1,
    startYear: int = 1907,
) -> tuple[list[pd.DataFrame], list[str]]:
    all_bird_series: list[pd.DataFrame] = []
    bird_names: list[str] = []

    key = "howMany" if how == "how_many" else "numberByPartyHours"

    with open(json_filename) as j:
        d = json.load(j)

        # out: {  bird_name: bird_name, x_years: [...years], y_how_many: [...howMany], y_by_party_hours: [...partyHours]}
        for bird_name, itemsByYear in d.items():
            byYearItems = [
                (year, datum)
                for (year, datum) in itemsByYear.items()
                if int(year) >= startYear
            ]

            bird_dict = {
                "x_years": [year for (year, _datum) in byYearItems],
                f"y_{how}": [
                    (noneValue if datum[key] is None else datum[key])
                    for (year, datum) in byYearItems
                ],
            }

            bird_df = pd.DataFrame(bird_dict)
            bird_df.loc[:, ["x_years", f"y_{how}"]]
            bird_df.set_index("x_years", inplace=True)

            all_bird_series.append(bird_df)
            bird_names.append(bird_name)

    return (all_bird_series, bird_names)


def bar_chart_to_dataframes(csv_filename: str):
    all_bird_series: list[pd.DataFrame] =[]
    bird_names: list[str] = []

    headers: list[str] = []

    # if I'm parsing this row by row, is a CSV reader the right choice?
    with open(csv_filename, newline="") as c:
        reader = csv.reader(c, delimiter="\t", skipinitialspace=True)
        # the csv sections end up separated by []

        for index, row in enumerate(reader):
            if index <= 9:
                # the first 10 lines are whitespace
                continue

            if index == 10:
                # the 10th row is the title
                continue

            if index == 11:
                # the 11th row is the number of taxa
                continue

            if index == 12:
                # empty row
                continue

            if index == 13:
                # header row!
                headers = row

                # this fills in the trailing december values
                headers += ["", "", ""]

                current_month = None

                for header_index, item in enumerate(row[1:]):
                    index_in_quartet = header_index % 4
                    if index_in_quartet == 0:
                        current_month = item

                    headers[header_index] = (
                        f"{current_month}_{index_in_quartet}"
                    )

                # this removes a final empty string from our header list
                headers.pop()

                continue

            if index == 14:
                # sample sizes
                continue

            if index == 15:
                # empty row
                continue

            if len(row) == 0:
                break;

            bird_name = row[0]
            values = row[1:]

            bird_dict = {
                "x_header_indices": [index for index, _ in enumerate(headers)],
                "y_abundance": [float(v) for v in values]
            }

            # print(bird_dict['x_header_indices'])
            # print(bird_dict['y_abundance'])

            bird_df = pd.DataFrame(bird_dict)
            bird_df.loc[:, ["x_header_indices", "y_abundance"]]
            bird_df.set_index("x_header_indices", inplace=True)

            all_bird_series.append(bird_df)
            bird_names.append(bird_name)

    return (all_bird_series, bird_names)
