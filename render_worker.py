import os
import subprocess
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace

from manim import config
from unit_square_animator import UnitSquareTransformation
from unit_cube_animator import CubeVertexTransformation
from TwoD_vector_animator import (
    TwoDVectorTransformation,
    TwoDVectorTransformationWithCoordinates,
)
from ThreeD_vector_animator import (
    ThreeDVectorTransformation,
    ThreeDVectorTransformationWithCoordinates,
)
from resources import app_data_path, linear_lab_videos_path


def configure_frozen_runtime():
    if not getattr(sys, "frozen", False):
        return

    bundle_directory = Path(sys._MEIPASS)
    os.environ["PATH"] = (
        str(bundle_directory)
        + os.pathsep
        + os.environ.get("PATH", "")
    )

    ffmpeg_path = bundle_directory / "ffmpeg.exe"
    ffprobe_path = bundle_directory / "ffprobe.exe"
    if ffmpeg_path.exists():
        os.environ["FFMPEG_BINARY"] = str(ffmpeg_path)
        try:
            from pydub import AudioSegment
            AudioSegment.converter = str(ffmpeg_path)
        except ImportError:
            pass
    if ffprobe_path.exists():
        os.environ["FFPROBE_BINARY"] = str(ffprobe_path)

    if sys.platform == "win32":
        from manim.utils import tex_file_writing

        if not getattr(tex_file_writing, "_linearlab_no_console", False):
            original_run = tex_file_writing.subprocess.run

            def run_without_console(*args, **kwargs):
                kwargs["creationflags"] = (
                    kwargs.get("creationflags", 0)
                    | subprocess.CREATE_NO_WINDOW
                )
                return original_run(*args, **kwargs)

            tex_file_writing.subprocess = SimpleNamespace(
                run=run_without_console
            )
            tex_file_writing._linearlab_no_console = True


def render_manim_request(request):
    configure_frozen_runtime()

    media_directory = app_data_path("media")
    tex_directory = app_data_path("tex")
    text_directory = app_data_path("text")

    config.preview = False
    config.quality = request["quality"]
    config.media_dir = str(media_directory)
    config.tex_dir = str(tex_directory)
    config.text_dir = str(text_directory)
    config.log_to_file = True
    config.log_dir = str(app_data_path("logs"))

    quality_folders = {
        "low_quality": "480p15",
        "medium_quality": "720p30",
        "high_quality": "1080p60",
    }
    quality_folder = quality_folders[request["quality"]]
    output_path = linear_lab_videos_path(
        quality_folder,
        request["output_file"],
    )
    config.output_file = str(output_path)

    kind = request["kind"]
    matrix = request["matrix"]
    show_inverse = request["show_inverse"]
    show_coordinates = request["show_coordinates"]
    vectors = request["vectors"]

    if kind == "unit_square":
        scene = UnitSquareTransformation(show_inverse, matrix=matrix)
    elif kind == "unit_cube":
        scene = CubeVertexTransformation(
            matrix,
            show_inverse=show_inverse,
            show_coordinates=show_coordinates,
        )
    elif kind == "2d_vector":
        scene_class = (
            TwoDVectorTransformationWithCoordinates
            if show_coordinates
            else TwoDVectorTransformation
        )
        scene = scene_class(show_inverse, matrix, vectors)
    elif kind == "3d_vector":
        scene_class = (
            ThreeDVectorTransformationWithCoordinates
            if show_coordinates
            else ThreeDVectorTransformation
        )
        scene = scene_class(show_inverse, matrix, vectors)
    else:
        raise ValueError(f"Unknown scene kind: {kind}")

    try:
        scene.render()
    except Exception:
        error_log_path = app_data_path("logs") / "render_errors.log"
        with error_log_path.open("a", encoding="utf-8") as error_log:
            error_log.write(traceback.format_exc())
            error_log.write("\n")
        raise
