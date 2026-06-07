import typing
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List

from PyQt6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, QObject,
                          Qt)


@dataclass
class WallpaperProperty:
    text: str
    type: str


@dataclass
class WallpaperBooleanProperty(WallpaperProperty):
    value: bool


@dataclass
class WallpaperSliderProperty(WallpaperProperty):
    min: int
    max: int
    value: int
    editable: bool


@dataclass
class WallpaperColorProperty(WallpaperProperty):
    value: str


@dataclass
class WallpaperFileProperty(WallpaperProperty):
    pass


@dataclass
class ComboOptions:
    label: str
    value: int


@dataclass
class WallpaperComboProperty(WallpaperProperty):
    options: List[ComboOptions]
    valie: int


@dataclass
class WallpaperTextinputProperty(WallpaperProperty):
    value: str


WallpaperPropertyType = (
    WallpaperProperty
    | WallpaperBooleanProperty
    | WallpaperSliderProperty
    | WallpaperColorProperty
    | WallpaperFileProperty
    | WallpaperComboProperty
)


class WallpaperType(Enum):
    SCENE = "scene"
    WEB = "web"
    VIDEO = "video"
    APP = "application"


@dataclass
class Wallpaper:
    contentrating: str
    file: Path
    properties: dict[str, WallpaperPropertyType]
    monetization: bool
    preview: Path
    tags: List[str]
    type: WallpaperType


class WallpapersModel(QAbstractListModel):
    ContentRatingRole = Qt.ItemDataRole.UserRole + 1
    FileRole = Qt.ItemDataRole.UserRole + 2
    PropertiesRole = Qt.ItemDataRole.UserRole + 3
    MonetizationRole = Qt.ItemDataRole.UserRole + 4
    PreviewRole = Qt.ItemDataRole.UserRole + 5
    TagsRole = Qt.ItemDataRole.UserRole + 6
    TypeRole = Qt.ItemDataRole.UserRole + 7

    def __init__(self, parent: typing.Optional[QObject] = None):
        super().__init__(parent)
        self._wallpapers: List[Wallpaper] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._wallpapers)

    def data(
        self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole
    ) -> typing.Any:
        if not index.isValid() or index.row() >= len(self._wallpapers):
            return None

        wallpaper = self._wallpapers[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            return wallpaper.file.name

        elif role == self.ContentRatingRole:
            return wallpaper.contentrating

        elif role == self.FileRole:
            return str(wallpaper.file)

        elif role == self.PropertiesRole:
            return wallpaper.properties

        elif role == self.MonetizationRole:
            return wallpaper.monetization

        elif role == self.PreviewRole:
            return str(wallpaper.preview)

        elif role == self.TagsRole:
            return wallpaper.tags

        return None

    def roleNames(self) -> dict[int, QByteArray]:
        return {
            Qt.ItemDataRole.DisplayRole: QByteArray(b"display"),
            self.ContentRatingRole: QByteArray(b"contentRating"),
            self.FileRole: QByteArray(b"file"),
            self.PropertiesRole: QByteArray(b"properties"),
            self.MonetizationRole: QByteArray(b"monetization"),
            self.PreviewRole: QByteArray(b"preview"),
            self.TagsRole: QByteArray(b"tags"),
            self.TypeRole: QByteArray(b"type"),
        }

    def get_wallpaper(self, index: int) -> Wallpaper:
        if 0 <= index < len(self._wallpapers):
            return self._wallpapers[index]
        raise IndexError(f"Index {index} out of range")

    def wallpapers(self) -> List[Wallpaper]:
        return self._wallpapers.copy()

    def count(self) -> int:
        return len(self._wallpapers)

    def clear(self):
        if self._wallpapers:
            self.beginResetModel()
            self._wallpapers.clear()
            self.endResetModel()

    def set_wallpapers(self, wallpapers: List[Wallpaper]):
        self.beginResetModel()
        self._wallpapers = wallpapers.copy()
        self.endResetModel()
