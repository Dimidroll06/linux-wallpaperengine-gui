from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, final

from PyQt6.QtCore import QObject, QProcess, QProcessEnvironment

from src.config import LIBRARY_COMMAND, STEAM_WALLPAPER_PATH
from src.models.wallpaper import Wallpaper


class ScalingMode(Enum):
    STRETCH = "stretch"
    FIT = "fit"
    FILL = "fill"
    DEFAULT = "default"


class ClampingMode(Enum):
    CLAMP = "clamp"
    BORDER = "border"
    REPEAT = "repeat"


@dataclass
class LibArguments:
    screen_root: str
    silent: bool = False
    volume: int = 100
    noautomute: bool = False
    no_audio_processing: bool = False
    fps: int = 24
    scaling: ScalingMode = field(default_factory=lambda: ScalingMode.DEFAULT)
    clamping: ClampingMode = field(default_factory=lambda: ClampingMode.BORDER)
    assets_dir: Path = field(default_factory=lambda: STEAM_WALLPAPER_PATH)
    disable_mouse: bool = False
    disable_paralax: bool = False
    no_fullscreen_pause: bool = False
    fullscreen_pause_only_active: bool = False
    fullscreen_api_ignore_app_id: List[int] = field(default_factory=lambda: [])


@final
class LibraryAPI(QObject):

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)

        self.target_path = LIBRARY_COMMAND

        # if not self.target_path.exists():
        #     print(
        #         f"[lib] Error: file ({self.target_path}) not found. Are you installed it?"
        #     )
        #     exit(1)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

        self.process.readyReadStandardOutput.connect(self._on_ready_read)
        self.process.finished.connect(self._on_finished)

    def start(self, args: LibArguments, wallpaper: Wallpaper):
        if self.process.state() != QProcess.ProcessState.NotRunning:
            print("[app] Process already running")
            return

        arguments = self._parse_args(args)
        # arguments.append("--bg")
        arguments.insert(
            0, str(wallpaper.file.parent.name)
        )  # TODO: Implement ID into Wallpaper class

        print(f"[lib] {self.target_path} {" ".join(arguments)}")
        self.process.start(self.target_path, arguments)

        if self.process.state() == QProcess.ProcessState.NotRunning:
            print(f"[lib] Error: proccess failed to run")
        else:
            print(
                f"[lib] Info: Process succesfully running (PID: {self.process.processId()})"
            )

    def take_screenshot(self, save_to: Path, wallpaper: Wallpaper) -> bool:
        process = QProcess(self)
        args = [
            "--bg",
            str(wallpaper.file.parent),
            "--screenshot",
            str(save_to.absolute()),
        ]
        process.start(self.target_path, args)

        process.waitForFinished(5000)

        if not process.state() == QProcess.ProcessState.NotRunning:
            print(f"[lib] Error: can't take screenshot :(")
            process.kill()
            process.waitForFinished(1000)
            return False

        if process.exitStatus() != QProcess.ExitStatus.NormalExit:
            print(f"[lib] Error: process for screenshots exited with error :(")
            return False

        return True

    def exit(self) -> bool:
        if self.process.state() == QProcess.ProcessState.NotRunning:
            print("[lib] Subprocess not running")
            return False

        self.process.terminate()

        if not self.process.waitForFinished(5000):
            print("[lib] Info: Process not answered to TERM signal. Trying to kill...")
            self.process.kill()
            self.process.waitForFinished(2000)

        return True

    def _on_ready_read(self) -> None:
        raw_data = self.process.readAllStandardOutput().data()
        text = raw_data.decode("utf-8", errors="replace")

        for line in text.splitlines():
            print(f"[lib] {line}")

    def _on_finished(self, exit_code: int, exit_status: QProcess.ExitStatus) -> None:
        print(
            f"[lib] Process finished with {exit_status.value} (status code {exit_code})"
        )

    def _parse_args(self, args: LibArguments) -> List[str]:
        args_list: List[str] = []

        if args.screen_root.strip():
            args_list.append("--screen-root")
            args_list.append(args.screen_root.strip())

        if args.silent:
            args_list.append("--silent")

        if max(min(args.volume, 100), 0) != 100:
            args_list.append("--volume")
            args_list.append(str(max(min(args.volume, 100), 0)))

        if args.noautomute:
            args_list.append("--noautomute")

        if args.no_audio_processing:
            args_list.append("--no-audio-processing")

        if max(args.fps, 0) != 0:
            args_list.append("--fps")
            args_list.append(str(args.fps))

        if args.scaling:
            args_list.append("--scaling")
            args_list.append(args.scaling.value)

        if args.clamping:
            args_list.append("--clamping")
            args_list.append(args.clamping.value)

        if args.disable_mouse:
            args_list.append("--disable-mouse")

        if args.disable_paralax:
            args_list.append("--disable-paralax")

        if args.no_fullscreen_pause:
            args_list.append("--no-fullscreen-pause")

        if args.fullscreen_pause_only_active:
            args_list.append("--fullscreen-pause-only-active")

        for appid in args.fullscreen_api_ignore_app_id:
            args_list.append("--fullscreen-pause-ignore-appid")
            args_list.append(str(appid))

        return args_list
