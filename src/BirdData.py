from typing import Literal, Sequence, cast
from app_types import BirdJSON, BirdName, RawCountDatum, Year


class BirdData:
    def __init__(self, json: BirdJSON) -> None:
        self.__raw_json__ = json

        self.bird_names = list(self.__raw_json__)
        self.years = self.__min_max_years__()

    def get_data_by_bird(
        self, bird_name: BirdName
    ) -> dict[Year, RawCountDatum]:
        if bird_name in self.bird_names:
            return self.__raw_json__[bird_name]
        else:
            raise Exception(f"<{bird_name}> not found in data")

    def get_by_bird(
        self,
        bird_name: BirdName,
        how: Literal["howMany"] | Literal["numberByPartyHours"],
    ) -> list[tuple[Year, float | None]]:
        if how != "howMany" and how != "numberByPartyHours":
            raise Exception('Which values must be "howMany" ')

        bird_data = self.get_data_by_bird(bird_name)

        result_list = [
            (year, datum[how]) for [year, datum] in bird_data.items()
        ]

        zipped = zip(*result_list)
        present_years: Sequence[Year] = list(zipped)[0]

        for req_year in self.years:
            if req_year not in present_years:
                year_pair = (cast(Year, req_year), None)
                result_list.append(year_pair)

        return result_list

    def __min_max_years__(self) -> range:
        all_years = [
            int(year)
            for bird_name in self.bird_names
            for year in list(self.__raw_json__[bird_name])
        ]

        min_year = min(all_years)
        max_year = max(all_years)

        return range(min_year, max_year + 1)
