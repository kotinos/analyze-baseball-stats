import math

import pandas as pd
import pytest

from baseball_stats.transforms import enrich_player_stats, top_high_value


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Name": ["A", "B", "C"],
            "AtBats": [100, 200, 50],
            "Hits": [30, 50, 10],
            "Walks": [20, 40, 10],
            "HitByPitch": [2, 0, 0],
            "SacrificeFlies": [3, 5, 1],
            "Salary": [1_000_000, 12_000_000, 500_000],
        }
    )


def test_enrich_player_stats_adds_obp_and_value() -> None:
    df = enrich_player_stats(_sample_frame())
    assert "OBP" in df.columns
    assert "Value" in df.columns
    assert len(df) == 3
    assert df.loc[0, "OBP"] == pytest.approx((30 + 20 + 2) / (100 + 20 + 2 + 3))


def test_top_high_value_returns_n_rows_sorted_desc() -> None:
    enriched = enrich_player_stats(_sample_frame())
    top = top_high_value(enriched, n=2)
    assert len(top) == 2
    values = top["Value"].tolist()
    assert all(values[i] >= values[i + 1] for i in range(len(values) - 1))


def test_top_high_value_puts_nan_last() -> None:
    df = pd.DataFrame(
        {
            "Name": ["High", "Low", "BadSalary"],
            "AtBats": [100, 100, 100],
            "Hits": [40, 10, 40],
            "Walks": [30, 5, 30],
            "HitByPitch": [0, 0, 0],
            "SacrificeFlies": [5, 5, 5],
            "Salary": [1_000_000, 20_000_000, 0],
        }
    )
    enriched = enrich_player_stats(df)
    top = top_high_value(enriched, n=3)
    assert top.iloc[-1]["Name"] == "BadSalary"
    assert math.isnan(top.iloc[-1]["Value"])
