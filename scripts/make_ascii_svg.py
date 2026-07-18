from pathlib import Path
import html

import yaml

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "generated" / "ascii.txt"
OUTPUT = ROOT / "assets" / "generated" / "ascii.svg"
THEME = ROOT / "config" / "theme.yaml"


def generate_svg(input_path=None, output_path=None, theme_path=None):
    """Render the ASCII portrait into a polished terminal-style SVG."""
    input_path = input_path or INPUT
    output_path = output_path or OUTPUT
    theme_path = theme_path or THEME

    lines = input_path.read_text(encoding="utf-8").splitlines()
    theme = yaml.safe_load(theme_path.read_text(encoding="utf-8")).get("theme", {})

    font_family = "'JetBrains Mono', 'Cascadia Code', Consolas, monospace"
    font_size = 9
    line_height = 11
    padding = 16
    border_radius = 14

    max_width = max(len(line) for line in lines) if lines else 40
    width = max_width * 6 + padding * 2 + 12
    height = len(lines) * line_height + padding * 2 + 24

    background = theme.get("background", "#0d1117")
    panel = theme.get("panel", "#161b22")
    primary = theme.get("secondary", "#58a6ff")
    text = theme.get("text", "#c9d1d9")
    muted = theme.get("muted", "#8b949e")

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>',
        'text { font-family: ' + font_family + '; white-space: pre; }',
        f'.ascii {{ fill: {text}; font-size: {font_size}px; }}',
        f'.label {{ fill: {primary}; font-size: 10px; letter-spacing: 0.04em; }}',
        '.fade { opacity: 0; animation: fadeIn 0.35s ease-out forwards; }',
        '@keyframes fadeIn { from { opacity: 0; transform: translateY(2px);} to { opacity: 1; transform: translateY(0);} }',
        '</style>',
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="{border_radius}" fill="{panel}" stroke="{muted}" stroke-opacity="0.28"/>',
        f'<rect x="12" y="12" width="{width - 24}" height="{height - 24}" rx="{border_radius - 4}" fill="{background}" />',
        f'<rect x="22" y="20" width="58" height="8" rx="4" fill="{primary}" opacity="0.16"/>',
        f'<rect x="22" y="20" width="18" height="8" rx="4" fill="{primary}" opacity="0.56"/>',
        f'<text x="22" y="36" class="label">ASCII PORTRAIT</text>',
    ]

    delay = 0.0
    for index, line in enumerate(lines):
        y = padding + 18 + index * line_height
        safe = html.escape(line)
        svg.append(
            f'<text x="{padding}" y="{y}" class="ascii fade" style="animation-delay:{delay:.2f}s;">{safe}</text>'
        )
        delay += 0.01

    svg.append('</svg>')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(svg), encoding="utf-8")
    return output_path


def main():
    output_path = generate_svg()
    print("ASCII SVG created!")
    print(output_path)


if __name__ == "__main__":
    main()