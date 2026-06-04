import signal
import sys
from os import getpid
from types import FrameType

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from src.gui.application import MyApp
from src.utils.singleton import is_already_running


def signal_handler(sig: int, _: FrameType | None):
    if sig == signal.SIGINT or sig == signal.SIGTERM:
        QApplication.quit()


def main():
    print(getpid())
    if is_already_running():
        print("Application is already running")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    app = MyApp()

    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    exit_code = app.exec()
    app.local_server.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
