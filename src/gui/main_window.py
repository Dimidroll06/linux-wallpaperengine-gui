from typing import final, override

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow


@final
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.force_close = False

    @override
    def closeEvent(self, a0: QCloseEvent | None):
        if not a0:
            return

        if self.force_close:
            a0.accept()
        else:
            a0.ignore()
            self.hide()
