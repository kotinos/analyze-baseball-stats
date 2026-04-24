import math

import pytest

from baseball_stats.metrics import obp_per_million, on_base_percentage


def test_on_base_percentage_standard_row() -> None:
    """Hand-checked OBP: (H+BB+HBP)/(AB+BB+HBP+SF)."""
    obp = on_base_percentage(
        hits=10,
        at_bats=40,
        walks=5,
        hit_by_pitch=1,
        sacrifice_flies=2,
    )
    assert obp == pytest.approx(16 / 48)


def test_on_base_percentage_zero_denominator_returns_nan() -> None:
    obp = on_base_percentage(
        hits=0,
        at_bats=0,
        walks=0,
        hit_by_pitch=0,
        sacrifice_flies=0,
    )
    assert math.isnan(obp)


def test_obp_per_million_higher_for_cheaper_same_obp() -> None:
    obp = 0.400
    assert obp_per_million(obp, 5_000_000) == pytest.approx(0.08)
    assert obp_per_million(obp, 10_000_000) == pytest.approx(0.04)
    assert obp_per_million(obp, 5_000_000) > obp_per_million(obp, 10_000_000)


def test_obp_per_million_non_positive_salary_returns_nan() -> None:
    assert math.isnan(obp_per_million(0.350, 0.0))
    assert math.isnan(obp_per_million(0.350, -1.0))


def test_obp_per_million_nan_obp_returns_nan() -> None:
    assert math.isnan(obp_per_million(float("nan"), 5_000_000))
