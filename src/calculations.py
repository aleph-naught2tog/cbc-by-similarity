from scipy.spatial.distance import cosine, directed_hausdorff

from typing import Literal

import numpy as np
from BirdData import BirdData
from app_types import BirdName
from transform_helpers import to_float_with_default


def calculate_hausdorff_distance(
    data: BirdData,
    comparison_bird_name: BirdName,
    how: Literal["howMany"] | Literal["numberByPartyHours"],
) -> list[tuple[str, float]]:
    bird_np = np.array(
        [
            (int(year), to_float_with_default(count))
            for (year, count) in data.get_by_bird(comparison_bird_name, how)
        ]
    )

    hausdorff_distances: list[tuple[str, float]] = []

    for bird_name in data.bird_names:
        counts = data.get_by_bird(bird_name, how)
        count_list = [
            (int(year), to_float_with_default(count))
            for (year, count) in counts
        ]

        np_counts = np.array(count_list)

        hausdorff_distances.append(
            (bird_name, directed_hausdorff(bird_np, np_counts)[0])
        )

    return hausdorff_distances


def calculate_cosine_similarities(
    data: BirdData,
    comparison_bird_name: BirdName,
    how: Literal["howMany"] | Literal["numberByPartyHours"],
) -> list[tuple[str, float]]:
    bird_list = [
        to_float_with_default(count)
        for (_year, count) in data.get_by_bird(comparison_bird_name, how)
    ]

    bird_np = np.array(bird_list)

    cosine_similarities: list[tuple[str, float]] = []

    for bird_name in data.bird_names:
        counts = data.get_by_bird(bird_name, how)

        # NOTE: we divide by 10 here to avoid scalar overflow
        count_list = [
            (to_float_with_default(count) / 100) for (_year, count) in counts
        ]
        np_counts = np.array(count_list)

        cosine_similarities.append((bird_name, 1 - cosine(bird_np, np_counts)))

    return cosine_similarities
