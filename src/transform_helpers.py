import json
import pandas as pd

from app_types import HowT

def json_to_dataframes(
    json_filename: str,
    how: HowT = "how_many",
    noneValue: int | float = -1,
) -> tuple[list[pd.DataFrame], list[str]]:
    all_bird_series: list[pd.DataFrame] = []
    bird_names: list[str] = []

    key = "howMany" if how == "how_many" else "numberByPartyHours"

    with open(json_filename) as j:
        d = json.load(j)

        # out: {  bird_name: bird_name, x_years: [...years], y_how_many: [...howMany], y_by_party_hours: [...partyHours]}
        for bird_name, itemsByYear in d.items():
            byYearItems = itemsByYear.items()
            bird_dict = {
                "x_years": [year for (year, _datum) in byYearItems],
                f"y_{how}": [
                    (noneValue if datum[key] is None else datum[key])
                    for (_year, datum) in byYearItems
                ],
            }

            bird_df = pd.DataFrame(bird_dict)
            bird_df.loc[:, ["x_years", f"y_{how}"]]
            bird_df.set_index("x_years", inplace=True)

            all_bird_series.append(bird_df)
            bird_names.append(bird_name)

    return (all_bird_series, bird_names)
