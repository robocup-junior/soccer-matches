import json
import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import yaml

CONFIG_FILE = Path("config.yaml")
DATA_DIR = Path("data")


def load_events() -> List[str]:
    """Load list of events from configuration file."""
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        events = config.get("events", [])
    else:
        env_events = os.getenv("EVENTS", "")
        events = [e.strip() for e in env_events.split(',') if e.strip()]
    return events


def fetch_matches(event: str) -> List[Dict[str, str]]:
    """Fetch match table from catigoal.com for given event."""
    url = f"https://catigoal.com/{event}/matches"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        return []

    headers = []
    for th in table.find_all("th"):
        colspan = int(th.get("colspan", 1))
        text = th.get_text(strip=True)
        if colspan > 1:
            for i in range(1, colspan + 1):
                headers.append(f"{text}_{i}")
        else:
            headers.append(text)
    rows = []
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        if not cells:
            continue

        expanded_cells = []
        for cell in cells:
            colspan = int(cell.get("colspan", 1))
            text = cell.get_text(strip=True)
            expanded_cells.extend([text] * colspan)

        row = {
            headers[i] if i < len(headers) else str(i): value
            for i, value in enumerate(expanded_cells)
        }
        rows.append(row)
    return rows


def save_matches(event: str, matches: List[Dict[str, str]]):
    event_dir = DATA_DIR / event
    event_dir.mkdir(parents=True, exist_ok=True)
    out_file = event_dir / "matches.json"
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)


def main() -> None:
    events = load_events()
    if not events:
        print("No events specified in configuration")
        return

    for event in events:
        try:
            matches = fetch_matches(event)
            save_matches(event, matches)
            print(f"Saved {len(matches)} matches for {event}")
        except Exception as exc:
            print(f"Failed to fetch matches for {event}: {exc}")


if __name__ == "__main__":
    main()
