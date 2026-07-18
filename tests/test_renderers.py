from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent.parent


def load_module(name, relative_path):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_ascii_svg_renderer_writes_svg(tmp_path):
    module = load_module("make_ascii_svg", "scripts/make_ascii_svg.py")
    output = tmp_path / "ascii.svg"
    module.OUTPUT = output
    module.INPUT = ROOT / "assets" / "generated" / "ascii.txt"
    module.generate_svg()
    content = output.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert "<rect" in content
    assert "</svg>" in content


def test_info_card_renderer_writes_svg(tmp_path):
    module = load_module("make_info_card", "scripts/make_info_card.py")
    output = tmp_path / "info-card.svg"
    module.OUTPUT = output
    module.PROFILE = ROOT / "config" / "profile.yaml"
    module.generate_svg()
    content = output.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert "neofetch" in content.lower()
    assert "</svg>" in content


def test_heatmap_renderer_writes_svg(tmp_path):
    module = load_module("render_heatmap_svg", "scripts/render_heatmap_svg.py")
    output = tmp_path / "contributions.svg"
    module.OUTPUT = output
    module.INPUT = ROOT / "assets" / "generated" / "contributions.json"
    module.render_svg()
    content = output.read_text(encoding="utf-8")
    assert content.startswith("<svg")
    assert "<rect" in content
    assert "</svg>" in content
