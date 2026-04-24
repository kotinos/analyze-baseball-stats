import pytest

from baseball_stats.mock_data import generate_players


def test_generate_players_rejects_wrong_count() -> None:
    with pytest.raises(ValueError, match="50"):
        generate_players(n=3, seed=1)
