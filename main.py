import json
from typing import NewType, TypedDict, cast
import numpy as np

# in:  { [birdName]: { year: { howMany, numberByPartyHours }}}
# out: bird_name,year,how_many,number_by_party_hours
#      .....

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.directed_hausdorff.html
# array

RawCountDatum = TypedDict(
    "RawCountDatum",
    {"howMany": float | None, "numberByPartyHours": float | None},
)
CountDatum = TypedDict(
    "CountDatum",
    {"how_many": float | None, "number_by_party_hours": float | None},
)


BirdJSON = NewType("BirdJSON", dict[str, dict[str, RawCountDatum]])


class BirdData:
    def __init__(self, json: BirdJSON) -> None:
        self.__raw_json__ = json

        self.bird_names = list(self.__raw_json__)
        self.years = list(self.__raw_json__[self.bird_names[0]])

    def get_by_bird(self, bird_name: str) -> dict[str, RawCountDatum]:
        if bird_name in self.bird_names:
            return self.__raw_json__[bird_name]
        else:
            raise Exception(f"<{bird_name}> not found in data")

    def get_counts_by_bird(
        self, bird_name: str
    ) -> list[tuple[str, float | None]]:
        bird_data = self.get_by_bird(bird_name)

        counts = [
            (year, datum["howMany"]) for [year, datum] in bird_data.items()
        ]

        return counts

    def get_party_hours_by_bird(
        self, bird_name: str
    ) -> list[tuple[str, float | None]]:
        bird_data = self.get_by_bird(bird_name)

        party_hours = [
            (year, datum["numberByPartyHours"])
            for [year, datum] in bird_data.items()
        ]

        return party_hours


def translate_json_to_bird_data(input_filename: str) -> BirdData:
    raw_json = {}

    with open(input_filename, newline="") as f:
        raw_json = json.load(f)

    bird_data = BirdData(raw_json)

    return bird_data


def main():
    input_filename = "data/raw/bird_map_as_json.json"

    bird_data = translate_json_to_bird_data(input_filename)

    print(bird_data.get_by_bird("Greater White-fronted Goose"))


if __name__ == "__main__":
    main()
