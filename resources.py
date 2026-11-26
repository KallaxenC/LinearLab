#resource_path finder so files can be found on different pc paths

from pathlib import Path
import sys
import os

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    return base_path / relative_path


def configure_frozen_stdio():
    if not getattr(sys, "frozen", False):
        return

    for stream_name in ("stdout", "stderr"):
        if getattr(sys, stream_name) is None:
            setattr(
                sys,
                stream_name,
                open(os.devnull, "w", encoding="utf-8"),
            )


def app_data_path(*parts):
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        base_path = Path(local_app_data) / "LinearLab"
    else:
        base_path = Path.home() / ".linearlab"

    result = base_path.joinpath(*parts)
    if parts:
        result.mkdir(parents=True, exist_ok=True)
    else:
        base_path.mkdir(parents=True, exist_ok=True)
    return result


def linear_lab_videos_path(*parts):
    base_path = Path.home() / "Videos" / "LinearLab"
    base_path.mkdir(parents=True, exist_ok=True)
    result = base_path.joinpath(*parts)
    result.parent.mkdir(parents=True, exist_ok=True)
    return result