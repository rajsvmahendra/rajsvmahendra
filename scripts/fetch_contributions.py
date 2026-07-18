from pathlib import Path
import json

import requests
from bs4 import BeautifulSoup

USERNAME = "rajsvmahendra"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "generated" / "contributions.json"

url = f"https://github.com/users/{USERNAME}/contributions"

print("Fetching contribution graph...")

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=20,
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

cells = soup.select("td.ContributionCalendar-day[data-date]")

days = []

for cell in cells:
    days.append({
        "date": cell["data-date"],
        "count": int(cell.get("data-level", 0)),
        "level": int(cell.get("data-level", 0)),
    })

# Fallback for older GitHub markup
if not days:
    rects = soup.select("rect[data-date]")

    for rect in rects:
        days.append({
            "date": rect["data-date"],
            "count": int(rect.get("data-count", 0)),
            "level": int(rect.get("data-level", 0)),
        })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

OUTPUT.write_text(
    json.dumps(days, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(days)} days.")
print(OUTPUT)