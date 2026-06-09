from typing import Optional, override

from PyQt6.QtCore import QEvent, QSize, Qt, pyqtSignal
from PyQt6.QtGui import (QEnterEvent, QMouseEvent, QPainter, QPaintEvent,
                         QPixmap, QResizeEvent)
from PyQt6.QtWidgets import (QGridLayout, QLabel, QScrollArea, QVBoxLayout,
                             QWidget)

from src.models.wallpaper import Wallpaper


class SquareImageLabel(QLabel):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("preview_wallpaper")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._pixmap: Optional[QPixmap] = None

    @override
    def setPixmap(self, a0: QPixmap) -> None:
        self._pixmap = a0
        self.update()

    @override
    def paintEvent(self, a0: Optional[QPaintEvent]) -> None:
        if not self._pixmap:
            return super().paintEvent(a0)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        widget_size = min(self.width(), self.height())

        scaled_pixmap = self._pixmap.scaled(
            widget_size,
            widget_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )

        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2

        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

    @override
    def sizeHint(self) -> QSize:
        return QSize(150, 150)

    @override
    def minimumSizeHint(self) -> QSize:
        return QSize(50, 50)


class WallpaperCard(QWidget):
    selected = pyqtSignal(Wallpaper)

    def __init__(self, wallpaper: Wallpaper, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("WallpaperCard")
        self.wallpaper = wallpaper
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.preview = SquareImageLabel()
        self._load_preview()

        self.name_label = QLabel(self.wallpaper.file.parent.name)  # TODO: Set to name
        self.name_label.setObjectName("name_label")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.preview)
        layout.addWidget(self.name_label)

    def _load_preview(self) -> None:
        try:
            pixmap = QPixmap(str(self.wallpaper.preview))
            if not pixmap.isNull():
                self.preview.setPixmap(pixmap)
            else:
                self.preview.setText("no preview")
        except Exception as e:
            print(
                f"[WallpaperCard] Error while loading pixmap for {self.wallpaper.preview}: {e}"
            )
            self.preview.setText("error")

    @override
    def mousePressEvent(self, a0: Optional[QMouseEvent]) -> None:
        if not a0:
            return

        if not a0.button() == Qt.MouseButton.LeftButton:
            self.selected.emit(self.wallpaper)
            self.setProperty("selected", True)
            style = self.style()
            if not style:
                return

            style.unpolish(self)
            style.polish(self)

    @override
    def enterEvent(self, event: Optional[QEnterEvent]) -> None:
        if not event:
            return

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    @override
    def leaveEvent(self, a0: Optional[QEvent]) -> None:
        if not a0:
            return
        self.unsetCursor()


class WallpaperGrid(QWidget):
    wallpaper_selected = pyqtSignal(Wallpaper)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.wallpapers = []
        self.base_card_size = 150
        self.cards = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(0, 0, 0, 0)

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def set_wallpapers(self, wallpapers: list[Wallpaper]):
        self.wallpapers = wallpapers
        self.rebuild_grid()

    def rebuild_grid(self):
        for card in self.cards:
            card.deleteLater()
        self.cards.clear()

        available_width = self.width() - 40
        columns = max(1, available_width // (self.base_card_size + 10))

        for idx, wallpaper in enumerate(self.wallpapers):
            card = WallpaperCard(wallpaper)
            card.selected.connect(self.wallpaper_selected.emit)
            card.setFixedSize(self.base_card_size, self.base_card_size)

            row, col = divmod(idx, columns)
            self.grid.addWidget(card, row, col)
            self.cards.append(card)

        self.grid.setRowStretch((len(self.wallpapers) // columns) + 1, 1)

    @override
    def resizeEvent(self, a0: Optional[QResizeEvent]) -> None:
        if not a0:
            return
        super().resizeEvent(a0)
        self.rebuild_grid()
