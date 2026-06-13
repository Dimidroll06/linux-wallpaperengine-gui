from typing import List, final, override

from PyQt6.QtGui import QCloseEvent, QScreen
from PyQt6.QtWidgets import QMainWindow

from src.core.lib import LibArguments, LibraryAPI, ScalingMode
from src.gui.widgets.wallpaper_grid import WallpaperGrid
from src.models.wallpaper import Wallpaper
from src.utils.wallpaper_loader import load_wallpapers


@final
class MainWindow(QMainWindow):
    def __init__(self, api: LibraryAPI, screens: List[QScreen]):
        super().__init__()
        self.force_close = False
        self.api = api
        self.wallpappers = load_wallpapers()
        self.screens = screens

        self.wallpaper_grid = WallpaperGrid()
        self.wallpaper_grid.wallpaper_selected.connect(self._wallpaper_choosed)
        self.setCentralWidget(self.wallpaper_grid)

        self.wallpaper_grid.set_wallpapers(self.wallpappers)

    def _wallpaper_choosed(self, wallpaper: Wallpaper):
        self.api.exit()

        args = LibArguments(self.screens[0].name(), scaling=ScalingMode.FILL)
        self.api.start(args, wallpaper)

    @override
    def closeEvent(self, a0: QCloseEvent | None):
        if not a0:
            return

        if self.force_close:
            self.api.exit()
            a0.accept()
        else:
            a0.ignore()
            self.hide()
