import sys
from typing import final

from PyQt6.QtGui import QIcon
from PyQt6.QtNetwork import QLocalServer
from PyQt6.QtWidgets import QApplication

from src.config import APPLICATION_NAME, ICON32_PATH
from src.gui.main_window import MainWindow
from src.gui.tray import TrayManager


@final
class MyApp(QApplication):
    def __init__(self):
        super().__init__([])
        self.local_server = QLocalServer()
        self.setWindowIcon(QIcon(str(ICON32_PATH)))

        if not self.local_server.listen(APPLICATION_NAME):
            print("Something went wrong")
            sys.exit(1)

        self.main_window = MainWindow()
        self.tray_manager = TrayManager(self.main_window)
