# Soccer Matches Extractor

This project scrapes soccer match information from `https://catigoal.com/{event}/matches` and
stores the data as JSON. The parser respects `colspan` attributes on both header and data
cells so tables are accurately mapped to JSON. When a header cell spans multiple columns,
each column is named sequentially (e.g. `Teams_1`, `Teams_2`, `Teams_3`).

## Setup

Install dependencies with [uv](https://github.com/astral-sh/uv):

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
