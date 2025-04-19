import argparse
import datetime
import json
import sys
import urllib.request
from pathlib import Path

# .config / local / state


STATS_DIR = Path.home() / ".local" / "state" / "obsidian-plugin-stats"

def fetch_stats(day_path):
    url = "https://raw.githubusercontent.com/obsidianmd/obsidian-releases/HEAD/community-plugin-stats.json"
    urllib.request.urlretrieve(url, day_path)

def fetch():
    # get day in utc
    today = datetime.datetime.utcnow().date()
    today_path = STATS_DIR / today.isoformat()
    if not (today_path).exists():
        fetch_stats(today_path)


def main():
    STATS_DIR.mkdir(exist_ok=True)

    if "--fetch" in sys.argv[1:]:
        fetch()
        return

    PARSER = argparse.ArgumentParser(description='Fetch and maintain stats about an Obsidian plugin')
    PARSER.add_argument("-V", '--versions', action='store_true', default=False, help="Show the versions for this plugin")
    PARSER.add_argument("-r", '--raw', action='store_true', default=False, help="Output raw JSON for this plugin")
    PARSER.add_argument("-t", '--timeseries', action='store_true', default=False, help="Output a timeseries of downloads")
    PARSER.add_argument('--fetch', action='store_true', default=False, help="Only fetch data")
    PARSER.add_argument('--date', type=datetime.date.fromisoformat, help="Return data for a particulary day rather than today")
    PARSER.add_argument('--json', action='store_true')
    PARSER.add_argument('plugin')
    args = PARSER.parse_args()


    today = datetime.datetime.utcnow().date()
    day = args.date or today
    day_path = STATS_DIR / day.isoformat()

    # read day_path as json
    try:
        with open(day_path, "r") as f:
            all_stats = json.load(f)
    except FileNotFoundError:
        if args.json:
            print(json.dumps({"error": "no-data", "message": f"No data for date {day.isoformat()}"}))
            return
        else:
            raise

    stats = all_stats[args.plugin]

    if args.fetch:
        return

    if args.raw:
        print(json.dumps(stats, indent=2))
        return

    if args.versions:
        print("\n".join(sorted(k for k in stats.keys() if k not in ("downloads", "updated"))))
        return

    if args.timeseries:
        for path in sorted(STATS_DIR.iterdir(), key=lambda x: x.name):
            with open(path) as stream:
                d = json.loads(stream.read())
            record = {"date": day.isoformat(), "downloads": d[args.plugin]["downloads"]}
            print(json.dumps(record))
        return

    if args.json:
        print(json.dumps({"downloads": stats["downloads"]}))
    else:
        print(stats["downloads"])











    # Fetch once daily
    # Fetch each run
