from typing import NewType, TypedDict

RawCountDatum = TypedDict(
    "RawCountDatum",
    {"howMany": float | None, "numberByPartyHours": float | None},
)

BirdName = NewType('BirdName', str)
Year = NewType('Year', str)

BirdJSON = NewType("BirdJSON", dict[BirdName, dict[Year, RawCountDatum]])

