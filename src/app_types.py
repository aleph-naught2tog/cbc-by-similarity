from typing import NewType, TypedDict

from plotters import Literal

RawCountDatum = TypedDict(
    "RawCountDatum",
    {"howMany": float | None, "numberByPartyHours": float | None},
)

BirdName = str

# NewType gives us a cast-er!
Year = NewType('Year', str)

BirdJSON = NewType("BirdJSON", dict[BirdName, dict[Year, RawCountDatum]])

JSONHowT = Literal["howMany"] | Literal["numberByPartyHours"]
HowT = Literal["how_many"] | Literal["by_party_hours"]
