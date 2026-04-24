from __future__ import annotations

import numpy as np
import pandas as pd

_PLAYER_NAMES: tuple[str, ...] = (
    "Miguel Vargas",
    "Jordan Walker",
    "Corbin Carroll",
    "Gunnar Henderson",
    "Elly De La Cruz",
    "James Wood",
    "Jackson Holliday",
    "Wyatt Langford",
    "Junior Caminero",
    "Evan Carter",
    "Pete Crow-Armstrong",
    "Marcelo Mayer",
    "Roman Anthony",
    "Curtis Mead",
    "Orelvis Martinez",
    "Kyle Manzardo",
    "Colt Keith",
    "Sal Frelick",
    "Tyler Soderstrom",
    "Dylan Crews",
    "Chandler Simpson",
    "Jacob Wilson",
    "Matt Shaw",
    "Luke Keaschall",
    "Jasson Dominguez",
    "Agustin Ramirez",
    "Endy Rodriguez",
    "Bo Naylor",
    "Harry Ford",
    "Ethan Salas",
    "Samuel Basallo",
    "Thomas Saggese",
    "Nolan Schanuel",
    "Joey Ortiz",
    "Brett Baty",
    "Zack Gelof",
    "Maikel Garcia",
    "Luisangel Acuna",
    "Jace Jung",
    "Brooks Lee",
    "Matt McLain",
    "Spencer Steer",
    "TJ Friedl",
    "Lawrence Butler",
    "Wilyer Abreu",
    "Jarred Kelenic",
    "Riley Greene",
    "Kerry Carpenter",
    "Riley Adams",
    "Tyler Freeman",
)


def generate_players(n: int = 50, seed: int | None = 42) -> pd.DataFrame:
    """Synthetic roster with realistic-ish counting stats and salaries."""
    if n != len(_PLAYER_NAMES):
        raise ValueError(f"n must be {len(_PLAYER_NAMES)} for the bundled name list")

    rng = np.random.default_rng(seed)
    at_bats = rng.integers(180, 640, size=n, endpoint=True)
    hit_rate = rng.uniform(0.22, 0.36, size=n)
    hits = np.minimum((at_bats * hit_rate).astype(int), at_bats - 1)
    walks = rng.integers(20, 110, size=n, endpoint=True)
    hit_by_pitch = rng.integers(0, 8, size=n, endpoint=True)
    sacrifice_flies = rng.integers(0, 10, size=n, endpoint=True)
    salary = np.round(rng.uniform(550_000, 28_000_000, size=n), -4)

    return pd.DataFrame(
        {
            "Name": list(_PLAYER_NAMES),
            "AtBats": at_bats,
            "Hits": hits,
            "Walks": walks,
            "HitByPitch": hit_by_pitch,
            "SacrificeFlies": sacrifice_flies,
            "Salary": salary,
        }
    )
