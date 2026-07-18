from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "generated" / "contributions.json"
OUTPUT = ROOT / "assets" / "generated" / "contributions.svg"


def load_days(input_path=INPUT):
    with open(input_path, encoding="utf-8") as handle:
        days = json.load(handle)

    days.sort(key=lambda day: day["date"])
    return days


def build_columns(days):
    columns = []
    current = []

    for day in days:
        current.append(day)
        if len(current) == 7:
            columns.append(current)
            current = []

    if current:
        while len(current) < 7:
            current.append(None)
        columns.append(current)

    return columns


def render_svg(input_path=None, output_path=None):
    """Render a polished GitHub-like contribution heatmap SVG."""
    input_path = input_path or INPUT
    output_path = output_path or OUTPUT

    days = load_days(input_path)
    columns = build_columns(days)

    cell = 10
    gap = 3
    left = 42
    top = 34

    colors = {
        0: "#161b22",
        1: "#0e4429",
        2: "#006d32",
        3: "#26a641",
        4: "#39d353",
    }

    width = left + len(columns) * (cell + gap) + 24
    height = top + 7 * (cell + gap) + 24

    month_positions = {}
    for col_index, week in enumerate(columns):
        for day in week:
            if day is None:
                continue
            dt = datetime.strptime(day["date"], "%Y-%m-%d")
            key = (dt.year, dt.month)
            if key not in month_positions:
                month_positions[key] = col_index

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    labels = {1: "Mon", 3: "Wed", 5: "Fri"}

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">' 
    )
    svg.append(
        '<style>'
        'text{fill:#8b949e;font-size:10px;font-family:Segoe UI,Arial,sans-serif;}'
        'rect{rx:2.4;ry:2.4;}'
        '</style>'
    )
    svg.append(f'<rect x="0" y="0" width="{width}" height="{height}" rx="16" fill="#0d1117"/>')
    svg.append(f'<rect x="16" y="16" width="{width - 32}" height="{height - 32}" rx="12" fill="#161b22" stroke="#30363d" stroke-opacity="0.5"/>')
    svg.append('<text x="28" y="32" fill="#58a6ff" font-size="11">Contribution activity</text>')

    for (year, month), col in month_positions.items():
        x = left + col * (cell + gap)
        svg.append(f'<text x="{x}" y="18">{months[month - 1]}</text>')

    for row, label in labels.items():
        y = top + row * (cell + gap) + cell - 2
        svg.append(f'<text x="8" y="{y}">{label}</text>')

    delay = 0.0
    for col_index, week in enumerate(columns):
        for row_index, day in enumerate(week):
            if day is None:
                continue
            x = left + col_index * (cell + gap)
            y = top + row_index * (cell + gap)
            level = int(day.get("level", 0))
            color = colors.get(level, colors[4])
            svg.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color}" opacity="0">'
                f'<animate attributeName="opacity" from="0" to="1" dur="0.22s" begin="{delay:.2f}s" fill="freeze"/>'
                '</rect>'
            )
            delay += 0.006

    svg.append('</svg>')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(svg), encoding="utf-8")
    return output_path


def main():
    output_path = render_svg()
    print("Contribution graph created!")
    print(output_path)


if __name__ == "__main__":
    main()
