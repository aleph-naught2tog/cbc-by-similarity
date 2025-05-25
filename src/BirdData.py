from typing import Literal
from app_types import BirdJSON, RawCountDatum


class BirdData:
    def __init__(self, json: BirdJSON) -> None:
        self.__raw_json__ = json

        self.bird_names = list(self.__raw_json__)
        self.years = self.__min_max_years__()

    def get_data_by_bird(self, bird_name: str) -> dict[str, RawCountDatum]:
        if bird_name in self.bird_names:
            return self.__raw_json__[bird_name]
        else:
            raise Exception(f"<{bird_name}> not found in data")

    def get_by_bird(
        self,
        bird_name: str,
        how: Literal["howMany"] | Literal["numberByPartyHours"],
    ):
        if how != "howMany" and how != "numberByPartyHours":
            raise Exception('Which values must be "howMany" ')

        bird_data = self.get_data_by_bird(bird_name)

        result_list = [
            (year, datum[how]) for [year, datum] in bird_data.items()
        ]

        present_years = list(zip(*result_list))[0]

        for req_year in self.years:
            if str(req_year) not in present_years:
                result_list.append((str(req_year), None))

        return result_list

    def __min_max_years__(self):
        all_years = [
            int(year)
            for bird_name in self.bird_names
            for year in list(self.__raw_json__[bird_name])
        ]

        min_year = min(all_years)
        max_year = max(all_years)

        return range(min_year, max_year + 1)
