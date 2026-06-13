import sys
from pathlib import Path
from typing import final

from PyQt6.QtGui import QIcon
from PyQt6.QtNetwork import QLocalServer
from PyQt6.QtWidgets import QApplication

from src.config import APPLICATION_NAME, ICON32_PATH
from src.core.lib import LibArguments, LibraryAPI
from src.core.state_manager import StateManager
from src.gui.main_window import MainWindow
from src.gui.tray import TrayManager
from src.models.wallpaper import Wallpaper


@final
class MyApp(QApplication):
    def __init__(self):
        super().__init__([])
        self.local_server = QLocalServer()
        self.setWindowIcon(QIcon(str(ICON32_PATH)))

        if not self.local_server.listen(APPLICATION_NAME):
            print("Something went wrong")
            sys.exit(1)

        self.load_styles()
        self.api = LibraryAPI()
        self.api.wallpaper_set.connect(self._safe_wallpaper)

        self.state_manger = StateManager()
        self.state = self.state_manger.load()

        if self.state.lastWallpaper and self.state.lastArgs:
            self.api.start(self.state.lastArgs, self.state.lastWallpaper)

        self.main_window = MainWindow(self.api, self.screens())
        self.tray_manager = TrayManager(self.main_window)

    def _safe_wallpaper(self, args: LibArguments, wallpaper: Wallpaper):
        self.state.lastArgs = args
        self.state.lastWallpaper = wallpaper
        self.state_manger.save(self.state)

    def load_styles(self):
        style_path = Path(__file__).parent / "resources" / "style.qss"
        if style_path.exists():
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
