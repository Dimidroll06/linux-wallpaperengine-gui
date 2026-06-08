from pathlib import Path

APPLICATION_NAME = "linux-wallpaper-engine-gui"

ICON32_PATH = Path(__file__).parent / "gui" / "resources" / "icon.png"
ICON512_PATH = Path(__file__).parent / "gui" / "resources" / "icon512.png"

STEAM_WALLPAPER_PATH = (
    Path.home() / ".steam" / "steam" / "steamapps" / "workshop" / "content" / "431960"
)
