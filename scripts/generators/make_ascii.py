from pathlib import Path

# pyrefly: ignore [missing-import]
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

INPUT = ROOT / "assets" / "profile.jpg"
OUTPUT = ROOT / "assets" / "ascii.txt"

ASCII = "@%#*+=-:. "

image = Image.open(INPUT).convert("L")

WIDTH = 80

w, h = image.size
ratio = h / w

HEIGHT = int(WIDTH * ratio * 0.55)

image = image.resize((WIDTH, HEIGHT))

pixels = image.load()

lines = []

for y in range(HEIGHT):
    line = ""

    for x in range(WIDTH):
        value = pixels[x, y]
        index = value * (len(ASCII) - 1) // 255
        line += ASCII[index]

    lines.append(line)

OUTPUT.write_text("\n".join(lines), encoding="utf-8")

print(f"Generated: {OUTPUT}")