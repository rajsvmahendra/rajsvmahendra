from pathlib import Path
import yaml

# Project root
ROOT = Path(__file__).resolve().parents[2]

# Important directories
ASSETS = ROOT / "assets"
CONFIG = ROOT / "config"
OUTPUT = ROOT / "output"

PROFILE_FILE = CONFIG / "profile.yaml"
THEME_FILE = CONFIG / "theme.yaml"


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


PROFILE = _load_yaml(PROFILE_FILE)
THEME = _load_yaml(THEME_FILE)