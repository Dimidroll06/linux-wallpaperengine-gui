from PyQt6.QtNetwork import QLocalSocket

from src.config import APPLICATION_NAME


def is_already_running() -> bool:
    socket = QLocalSocket()
    socket.connectToServer(APPLICATION_NAME)

    if socket.waitForConnected(500):
        socket.close()
        return True

    return False
