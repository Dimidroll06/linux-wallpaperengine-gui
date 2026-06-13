import typing
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field, model_validator
from PyQt6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, QObject,
                          Qt)


class WallpaperProperty(BaseModel):
    text: str
    type: str


class WallpaperBooleanProperty(WallpaperProperty):
    value: bool


class WallpaperSliderProperty(WallpaperProperty):
    min: float
    max: float
    value: float
    editable: bool


class WallpaperColorProperty(WallpaperProperty):
    value: str


class WallpaperFileProperty(WallpaperProperty):
    pass


class ComboOptions(BaseModel):
    label: str
    value: Any


class WallpaperComboProperty(WallpaperProperty):
    options: List[ComboOptions]
    value: Any


class WallpaperTextinputProperty(WallpaperProperty):
    value: str


WallpaperPropertyType = Union[
    WallpaperBooleanProperty,
    WallpaperSliderProperty,
    WallpaperColorProperty,
    WallpaperFileProperty,
    WallpaperComboProperty,
    WallpaperTextinputProperty,
    WallpaperProperty,
]


class WallpaperType(Enum):
    SCENE = "scene"
    WEB = "web"
    VIDEO = "video"
    APP = "application"


class Wallpaper(BaseModel):
    contentrating: str = "Everyone"
    file: Path = Path()
    properties: Dict[str, Any] = Field(default_factory=dict)
    monetization: bool = False
    preview: Path = Path()
    tags: List[str] = Field(default_factory=list)
    type: WallpaperType = WallpaperType.SCENE

    @model_validator(mode="before")
    @classmethod
    def _parse_properties(cls, data: Any) -> Any:
        if isinstance(data, dict) and "properties" in data:
            props = data["properties"]
            if isinstance(props, dict):
                parsed_props = {}
                for key, prop_data in props.items():
                    if isinstance(prop_data, dict):
                        p_type = prop_data.get("type", "").lower()

                        if p_type == "boolean":
                            parsed_props[key] = WallpaperBooleanProperty(**prop_data)
                        elif p_type == "slider":
                            parsed_props[key] = WallpaperSliderProperty(**prop_data)
                        elif p_type == "color":
                            parsed_props[key] = WallpaperColorProperty(**prop_data)
                        elif p_type == "file":
                            parsed_props[key] = WallpaperFileProperty(**prop_data)
                        elif p_type == "combo":
                            parsed_props[key] = WallpaperComboProperty(**prop_data)
                        elif p_type == "textinput":
                            parsed_props[key] = WallpaperTextinputProperty(**prop_data)
                        else:
                            parsed_props[key] = WallpaperProperty(**prop_data)
                    else:
                        parsed_props[key] = prop_data

                data["properties"] = parsed_props
        return data


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
