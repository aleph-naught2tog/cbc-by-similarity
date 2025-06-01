import json
from BirdData import BirdData
import pandas as pd


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


# NOTE: we are coercing None to -1
def json_to_dataframes(
    json_filename: str,
) -> tuple[list[pd.DataFrame], list[str]]:
    all_bird_series: list[pd.DataFrame] = []
    bird_names: list[str] = []

    with open(json_filename) as j:
        d = json.load(j)

        # out: {  bird_name: bird_name, x_years: [...years], y_how_many: [...howMany], y_by_party_hours: [...partyHours]}
        for bird_name, itemsByYear in d.items():
            byYearItems = itemsByYear.items()
            bird_dict = {
                # "bird_name": bird_name,
                "x_years": [year for (year, _datum) in byYearItems],
                "y_how_many": [
                    (-1 if datum["howMany"] is None else datum["howMany"])
                    for (_year, datum) in byYearItems
                ],
                # "y_by_party_hours": [
                #     (
                #         -1
                #         if datum["numberByPartyHours"] is None
                #         else datum["numberByPartyHours"]
                #     )
                #     for (_year, datum) in byYearItems
                # ],
            }

            bird_df = pd.DataFrame(bird_dict)
            bird_df.loc[:, ["x_years", "y_how_many"]]
            bird_df.set_index("x_years", inplace=True)  # type: ignore bc/3rd party

            all_bird_series.append(bird_df)
            bird_names.append(bird_name)

    return (all_bird_series, bird_names)
