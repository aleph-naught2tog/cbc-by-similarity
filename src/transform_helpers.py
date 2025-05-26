import json
from BirdData import BirdData


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
