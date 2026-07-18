from pathlib import Path
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from rembg import remove


# -----------------------------
# Paths
# -----------------------------
ROOT = Path(__file__).resolve().parent.parent

INPUT_IMAGE = ROOT / "assets" / "profile.jpg"
OUTPUT_IMAGE = ROOT / "assets" / "generated" / "source-prepped.png"


# -----------------------------
# Step 1 : Remove Background
# -----------------------------
print("[1/4] Removing background...")

input_bytes = INPUT_IMAGE.read_bytes()
output_bytes = remove(input_bytes)

from io import BytesIO

rgba = Image.open(BytesIO(output_bytes)).convert("RGBA")
rgba = np.array(rgba)


# -----------------------------
# Step 2 : White Background
# -----------------------------
print("[2/4] Applying white background...")

background = np.ones((rgba.shape[0], rgba.shape[1], 3), dtype=np.uint8) * 255

alpha = rgba[:, :, 3] / 255.0

for c in range(3):
    background[:, :, c] = (
        alpha * rgba[:, :, c] +
        (1 - alpha) * background[:, :, c]
    )

image = background.astype(np.uint8)


# -----------------------------
# Step 3 : CLAHE Contrast
# -----------------------------
print("[3/4] Enhancing contrast...")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(
    clipLimit=2.5,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)


# -----------------------------
# Step 4 : Save
# -----------------------------
print("[4/4] Saving...")

OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)

cv2.imwrite(str(OUTPUT_IMAGE), gray)

print()
print("Done!")
print(OUTPUT_IMAGE)