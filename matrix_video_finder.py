from pathlib import Path

def find_matrix_video(file_type,quality,values):
    if quality == "low_quality":
        quality_folder = "480p15"
    elif quality == "medium_quality":
        quality_folder = "720p30"
    elif quality == "high_quality":
        quality_folder = "1080p60"

    expected_filename = f"matrix_animation_{values}_{file_type}.mp4"

    script_dir = Path(__file__).resolve().parent

    video_file_path = script_dir / "media" / "videos" / quality_folder / expected_filename

    if video_file_path.exists():
        return str(video_file_path)
    else:
        return None