"""
Boot-time ASCII splash art.

Two sources feed the random pool:
  1. Hand-authored static banners loaded from ui/banner_art/*.txt
     (edit/add files there - no code changes needed).
  2. Procedurally generated banners via pyfiglet, using a random font
     from a curated list and the same rich color language as the
     static set, giving effectively unlimited variation.

Falls back gracefully to the static set if pyfiglet isn't installed.
"""

import random
from pathlib import Path

BANNER_ART_DIR = Path(__file__).parent / "banner_art"

TAGLINE = "--- Security Footprint & Network Leak Guard ---"

try:
    import pyfiglet
    PYFIGLET_AVAILABLE = True
except ImportError:
    PYFIGLET_AVAILABLE = False

# Fonts chosen for readability at typical terminal widths.
FIGLET_FONTS = ["slant", "ansi_shadow", "doom", "big", "standard", "chunky"]

# Color pairs (top-half, bottom-half) matched to the existing palette
# used across the static banners so generated art blends in.
COLOR_PAIRS = [
    ("bold cyan", "bold blue"),
    ("bold red", "bold yellow"),
    ("bold green", "bold white"),
    ("bold magenta", "bold violet"),
    ("bold blue", "bold magenta"),
]


def _load_static_banners() -> list[str]:
    banners = []
    if BANNER_ART_DIR.exists():
        for path in sorted(BANNER_ART_DIR.glob("*.txt")):
            banners.append(path.read_text())
    return banners


def _generate_figlet_banner() -> str:
    font = random.choice(FIGLET_FONTS)
    top_color, bottom_color = random.choice(COLOR_PAIRS)
    art = pyfiglet.figlet_format("NETLEAK GUARD", font=font)

    lines = [line for line in art.split("\n") if line.strip()]
    mid = len(lines) // 2
    colored = (
        [f"[{top_color}]{line}[/{top_color}]" for line in lines[:mid]]
        + [f"[{bottom_color}]{line}[/{bottom_color}]" for line in lines[mid:]]
    )
    colored.append(f"      [bold white]{TAGLINE}[/bold white]")
    return "\n".join(colored)


def show_random_banner(console):
    pool = _load_static_banners()

    # Bias toward generated banners when available - they add real
    # variety on top of the fixed set rather than just cycling 4 strings.
    if PYFIGLET_AVAILABLE:
        try:
            pool.append(_generate_figlet_banner())
            pool.append(_generate_figlet_banner())
        except Exception:
            pass  # fall back to whatever static banners exist

    if not pool:
        console.print("[bold cyan]NETLEAK GUARD[/bold cyan]")
        return

    console.print(random.choice(pool))
