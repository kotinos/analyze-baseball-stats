from __future__ import annotations

import math


def on_base_percentage(
    hits: int,
    at_bats: int,
    walks: int,
    hit_by_pitch: int,
    sacrifice_flies: int,
) -> float:
    """Standard OBP = (H + BB + HBP) / (AB + BB + HBP + SF)."""
    numerator = hits + walks + hit_by_pitch
    denominator = at_bats + walks + hit_by_pitch + sacrifice_flies
    if denominator == 0:
        return float("nan")
    return numerator / denominator


def obp_per_million(obp: float, salary: float) -> float:
    """OBP per $1M salary — higher means more on-base skill per payroll dollar."""
    if salary <= 0 or math.isnan(obp):
        return float("nan")
    millions = salary / 1_000_000.0
    return obp / millions
