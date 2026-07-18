from pathlib import Path
import html

import yaml

ROOT = Path(__file__).resolve().parent.parent

PROFILE = ROOT / "config" / "profile.yaml"
THEME = ROOT / "config" / "theme.yaml"
OUTPUT = ROOT / "assets" / "generated" / "info-card.svg"


def wrap_text(text, max_chars):
    words = text.split()
    lines = []
    current = []
    current_len = 0

    for word in words:
        if current_len + len(word) + (1 if current else 0) <= max_chars:
            current.append(word)
            current_len += len(word) + (1 if current_len else 0)
        else:
            lines.append(" ".join(current) if current else word)
            current = [word]
            current_len = len(word)

    if current:
        lines.append(" ".join(current))

    return lines


def build_sections(data):
    lines = []
    lines.append(("Name", data["name"]))
    lines.append(("Role", " • ".join(data["role"])))
    lines.append(("", ""))

    edu = data["education"]
    lines.append(("Education", edu["degree"]))
    lines.append(("", f'{edu["university"]} ({edu["graduation"]})'))
    lines.append(("", ""))

    sections = [
        ("Languages", "languages"),
        ("Frontend", "frontend"),
        ("Backend", "backend"),
        ("Android", "android"),
        ("Data Science", "data_science"),
        ("Projects", "projects"),
        ("Certs", "certifications"),
    ]

    for title, key in sections:
        value = ", ".join(data[key])
        lines.append((title, value))

    return lines


def generate_svg(profile_path=None, output_path=None, theme_path=None):
    """Render a neofetch-inspired terminal card with automatic wrapping."""
    profile_path = profile_path or PROFILE
    output_path = output_path or OUTPUT
    theme_path = theme_path or THEME

    data = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    theme = yaml.safe_load(theme_path.read_text(encoding="utf-8")).get("theme", {})

    lines = build_sections(data)

    padding = 24
    label_width = 104
    line_height = 18
    width = 740
    height = 48 + len(lines) * line_height + 26

    background = theme.get("background", "#0d1117")
    panel = theme.get("panel", "#161b22")
    primary = theme.get("secondary", "#58a6ff")
    text = theme.get("text", "#c9d1d9")
    muted = theme.get("muted", "#8b949e")
    success = theme.get("success", "#3fb950")

    content_x = padding + label_width + 12
    max_value_chars = 48

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" fill="{panel}" stroke="{muted}" stroke-opacity="0.28"/>',
        f'<rect x="16" y="16" width="{width - 32}" height="{height - 32}" rx="12" fill="{background}"/>',
        f'<rect x="28" y="32" width="46" height="8" rx="4" fill="{success}" opacity="0.9"/>',
        f'<rect x="82" y="32" width="46" height="8" rx="4" fill="{primary}" opacity="0.9"/>',
        f'<rect x="136" y="32" width="46" height="8" rx="4" fill="{muted}" opacity="0.9"/>',
        f'<text x="{padding}" y="64" font-family="JetBrains Mono, Consolas, monospace" font-size="16" fill="{primary}">rajsv@github:~$ neofetch</text>',
        f'<text x="{padding}" y="86" font-family="JetBrains Mono, Consolas, monospace" font-size="12" fill="{muted}">System information • profile generator</text>',
    ]

    y = 112
    for label, value in lines:
        if label == "" and value == "":
            y += 4
            continue

        if label:
            svg.append(
                f'<text x="{padding}" y="{y}" font-family="JetBrains Mono, Consolas, monospace" font-size="13" fill="{success}">{html.escape(label)}</text>'
            )

        wrapped = wrap_text(value, max_value_chars)
        for index, chunk in enumerate(wrapped):
            chunk_y = y + index * 16
            svg.append(
                f'<text x="{content_x}" y="{chunk_y}" font-family="JetBrains Mono, Consolas, monospace" font-size="13" fill="{text}">{html.escape(chunk)}</text>'
            )

        y += max(18, len(wrapped) * 16)

    svg.append('</svg>')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(svg), encoding="utf-8")
    return output_path


def main():
    output_path = generate_svg()
    print("Info card created!")
    print(output_path)


if __name__ == "__main__":
    main()