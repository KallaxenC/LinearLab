from pathlib import Path

def find_matrix_video_2D(quality, a, b, c, d):
    if quality == "low_quality":
        quality_folder = "480p15"
    elif quality == "medium_quality":
        quality_folder = "720p30"
    elif quality == "high_quality":
        quality_folder = "1080p60"
    expected_filename = f"matrix_animation_{a}{b}{c}{d}.mp4"

    script_dir = Path(__file__).resolve().parent

    video_file_path = script_dir / "media" / "videos" / quality_folder / expected_filename
    #video_file_path = script_dir / "media" / "videos" / "720p30" / expected_filename
    if video_file_path.exists():
        return str(video_file_path)
    else:
        return None

def find_matrix_video_3D(quality, a, b, c, d, e, f, g, h, i):
    if quality == "low_quality":
        quality_folder = "480p15"
    elif quality == "medium_quality":
        quality_folder = "720p30"
    elif quality == "high_quality":
        quality_folder = "1080p60"

    expected_filename = f"matrix_animation_{a}{b}{c}{d}{e}{f}{g}{h}{i}.mp4"

    script_dir = Path(__file__).resolve().parent

    video_file_path = script_dir / "media" / "videos" / quality_folder / expected_filename

    if video_file_path.exists():
        return str(video_file_path)
    else:
        return None