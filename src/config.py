from pathlib import Path

APPLICATION_NAME = "linux-wallpaper-engine-gui"

ICON32_PATH = Path(__file__).parent / "gui" / "resources" / "icon.png"
ICON512_PATH = Path(__file__).parent / "gui" / "resources" / "icon512.png"

STEAM_WALLPAPER_PATH = (
    Path.home() / ".steam" / "steam" / "steamapps" / "workshop" / "content" / "431960"
)

USE_ONLY_VIDEO_WALLPAPERS = (
    True  # set false to show all wallpapers (many of them not supported yet)
)
LIBRARY_COMMAND = "linux-wallpaperengine"
