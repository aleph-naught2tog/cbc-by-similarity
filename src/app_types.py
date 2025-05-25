from typing import NewType, TypedDict

RawCountDatum = TypedDict(
    "RawCountDatum",
    {"howMany": float | None, "numberByPartyHours": float | None},
)

BirdJSON = NewType("BirdJSON", dict[str, dict[str, RawCountDatum]])

