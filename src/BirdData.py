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

        present_years = list(zip(*counts))[0]

        for req_year in self.years:
            if str(req_year) not in present_years:
                counts.append((str(req_year), None))

        print(counts)

        return counts

    def get_party_hours_by_bird(
        self, bird_name: str
    ) -> list[tuple[str, float | None]]:
        bird_data = self.get_by_bird(bird_name)

        party_hours = [
            (year, datum["numberByPartyHours"])
            for [year, datum] in bird_data.items()
        ]

        present_years = list(zip(*party_hours))[0]

        for req_year in self.years:
            if str(req_year) not in present_years:
                party_hours.append((str(req_year), None))

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
