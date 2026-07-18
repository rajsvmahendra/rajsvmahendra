from pathlib import Path

from PIL import Image

# ---------------------------------
# Paths
# ---------------------------------
ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "assets" / "generated" / "source-prepped.png"
OUTPUT = ROOT / "assets" / "generated" / "ascii.txt"

# ---------------------------------
# Settings
# ---------------------------------
WIDTH = 110
ASCII = "@$B%8&WM#*oahkbdpqwmZO0QLCJYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def generate_ascii(input_path=None, output_path=None, width=WIDTH):
    """Convert a grayscale portrait into a readable ASCII art preview."""
    input_path = input_path or INPUT
    output_path = output_path or OUTPUT

    img = Image.open(input_path).convert("L")
    source_width, source_height = img.size
    aspect = source_height / source_width
    new_height = max(24, int(width * aspect * 0.58))

    img = img.resize((width, new_height), Image.LANCZOS)
    pixels = list(img.getdata())

    lines = []
    for y in range(new_height):
        row = []
        for x in range(width):
            value = pixels[y * width + x]
            index = value * (len(ASCII) - 1) // 255
            row.append(ASCII[index])
        lines.append("".join(row))

    ascii_art = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(ascii_art, encoding="utf-8")
    return output_path


def main():
    output_path = generate_ascii()
    print("ASCII generated!")
    print(output_path)


if __name__ == "__main__":
    main()