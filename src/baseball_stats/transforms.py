from __future__ import annotations

import pandas as pd

from baseball_stats.metrics import obp_per_million, on_base_percentage


def enrich_player_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return a new frame with OBP and Value (OBP per $1M salary)."""
    result = df.copy()
    obps: list[float] = []
    values: list[float] = []
    for row in result.itertuples(index=False):
        obp = on_base_percentage(
            int(row.Hits),
            int(row.AtBats),
            int(row.Walks),
            int(row.HitByPitch),
            int(row.SacrificeFlies),
        )
        obps.append(obp)
        values.append(obp_per_million(obp, float(row.Salary)))
    result["OBP"] = obps
    result["Value"] = values
    return result


def top_high_value(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Highest Value first; rows with NaN value sort last."""
    sorted_df = df.sort_values("Value", ascending=False, na_position="last")
    return sorted_df.head(n).reset_index(drop=True)
