import os
from pathlib import Path
from typing import Optional

APPLICATION_NAME: str = "linux-wallpaper-engine-gui"

ICON32_PATH: Path = Path(__file__).parent / "gui" / "resources" / "icon.png"
ICON512_PATH: Path = Path(__file__).parent / "gui" / "resources" / "icon512.png"

STEAM_WALLPAPER_PATH: Path = (
    Path.home() / ".steam" / "steam" / "steamapps" / "workshop" / "content" / "431960"
)

USE_ONLY_VIDEO_WALLPAPERS: bool = (
    True  # set false to show all wallpapers (many of them not supported yet)
)
LIBRARY_COMMAND: str = "linux-wallpaperengine"

XDG_CONFIG_HOME: Optional[str] = os.environ.get("XDG_CONFIG_HOME")
APP_STATE_PATH: Path = (
    Path(XDG_CONFIG_HOME) if XDG_CONFIG_HOME else Path.home()
) / ".linux-wallpaper-engine-gui.json"
