from typing import cast
from app_types import BirdJSON, RawCountDatum


class BirdData:
    def __init__(self, json: BirdJSON) -> None:
        self.__raw_json__ = json

        self.bird_names = list(self.__raw_json__)
        self.years = self.__min_max_years__()

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

    def __min_max_years__(self):
        all_years = [
            int(year)
            for bird_name in self.bird_names
            for year in list(self.__raw_json__[bird_name])
        ]

        min_year = min(all_years)
        max_year = max(all_years)

        return range(min_year, max_year + 1)

    # this isn't working
    # def __process_json__(self):
    #     processed_json: BirdJSON = cast(BirdJSON, {})

    #     for required_year in self.years:
    #         print(required_year)
    #         for bird_name, year_data in self.__raw_json__.items():
    #             processed_year_data = year_data.copy()

    #             if str(required_year) not in processed_year_data:
    #                 print(f'{required_year} gone')
    #                 processed_year_data.update({ str(required_year): {
    #                         "howMany": None,
    #                         "numberByPartyHours": None,
    #                     } })
    #             else:
    #                 print(f'{required_year} present')

    #             # print(processed_year_data)

    #             processed_json.update({ bird_name: processed_year_data })

    #     return processed_json
