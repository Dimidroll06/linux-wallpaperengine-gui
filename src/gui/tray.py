from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from src.config import ICON32_PATH
from src.gui.main_window import MainWindow


class TrayManager:
    def __init__(self, main_window: MainWindow):
        self.main_window = main_window
        self.tray = QSystemTrayIcon()

        self.icon = QIcon(str(ICON32_PATH))

        self.menu = QMenu()
        self.show_action = QAction("Show window")
        self.show_action.triggered.connect(self.main_window.show)

        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit_app)

        self.menu.addAction(self.show_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)

        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)

        # Wayland fix :)
        QTimer.singleShot(150, self.show_icon)

    def show_icon(self):
        self.tray.setIcon(self.icon)
        self.tray.show()

    def quit_app(self):
        self.main_window.force_close = True
        self.main_window.close()
        QApplication.quit()

    def show_message(self, text):
        self.tray.showMessage(
            "Status: ", text, QSystemTrayIcon.MessageIcon.Information, 2000
        )
