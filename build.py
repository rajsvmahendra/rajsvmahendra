import subprocess
import sys


def run_pipeline():
    scripts = [
        "scripts/prep_photo.py",
        "scripts/make_ascii.py",
        "scripts/make_ascii_svg.py",
        "scripts/make_info_card.py",
        "scripts/fetch_contributions.py",
        "scripts/render_heatmap_svg.py",
    ]

    for script in scripts:
        print(f"\n▶ Running {script}")
        subprocess.run([sys.executable, script], check=True)

    print("\n✅ All assets generated successfully!")


if __name__ == "__main__":
    run_pipeline()