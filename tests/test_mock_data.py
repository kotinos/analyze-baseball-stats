from baseball_stats.mock_data import generate_players
from baseball_stats.transforms import enrich_player_stats, top_high_value


def test_generate_players_default_count_and_columns() -> None:
    df = generate_players(seed=42)
    assert len(df) == 50
    for col in (
        "Name",
        "AtBats",
        "Hits",
        "Walks",
        "HitByPitch",
        "SacrificeFlies",
        "Salary",
    ):
        assert col in df.columns


def test_pipeline_reproducible_with_seed() -> None:
    a = top_high_value(enrich_player_stats(generate_players(seed=7)), n=5)
    b = top_high_value(enrich_player_stats(generate_players(seed=7)), n=5)
    assert a["Name"].tolist() == b["Name"].tolist()
