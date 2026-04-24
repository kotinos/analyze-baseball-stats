# Analyze Baseball Stats

Moneyball-style **Streamlit** dashboard: synthetic roster (50 players), **OBP**, and **OBP per $1M salary** to spotlight high-value bats—no CSVs.

## Quick start

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Use the sidebar **Mock seed** to reshuffle stats. If `streamlit` is not on `PATH`, prefer `python -m streamlit` as above.

## What you get

- **Top 5** leaderboard (styled table: stronger greens = better value)
- **Scatter**: salary vs OBP, hover shows name + key numbers
- **Dark** UI tuned for a “war room” feel

## Tests

```bash
python -m pytest tests/ --cov=baseball_stats --cov-report=term-missing
```

## Stack

Python · Streamlit · Pandas · Plotly · pytest
