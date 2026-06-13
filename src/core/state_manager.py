from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.config import APP_STATE_PATH
from src.core.lib import LibArguments
from src.models.wallpaper import Wallpaper


class AppState(BaseModel):
    lastWallpaper: Optional[Wallpaper] = None
    lastArgs: Optional[LibArguments] = None

    def save(self, filepath: Path):
        json_data = self.model_dump_json(indent=4, ensure_ascii=False)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_data)

    @classmethod
    def load(cls, filepath: Path) -> AppState:
        if not filepath.exists():
            return cls()

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return cls.model_validate_json(f.read())
        except Exception as e:
            print(f"[app] Error while loading state ({e}), using default config.")
            return cls()


class StateManager:
    def __init__(self):
        self.filepath = APP_STATE_PATH

    def save(self, state: AppState):
        state.save(self.filepath)

    def load(self) -> AppState:
        if not self.filepath.exists():
            return AppState()

        return AppState.load(self.filepath)
