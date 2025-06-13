# Soccer Matches Extractor

This project scrapes soccer match information from `https://catigoal.com/{event}/matches` and
stores the data as JSON.

## Setup

Install dependencies with [uv](https://github.com/astral-sh/uv):

```bash
uv pip install -r requirements.txt
```

Or using `uv` directly with the `pyproject.toml`:

```bash
uv pip install -e .
```

## Configuration

Specify a list of events in `config.yaml`:

```yaml
events:
  - RCJE2025
  - OTHEREVENT
```

## Usage

Run the fetcher to download match tables and store them under `data/{event}/matches.json`:

```bash
python -m soccer_matches.fetch
```

Alternatively specify events via an environment variable:

```bash
EVENTS=RCJE2025 python -m soccer_matches.fetch
```

Note that access to `catigoal.com` may require an internet connection.
