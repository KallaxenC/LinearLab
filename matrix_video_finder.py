from pathlib import Path
from resources import linear_lab_videos_path

def find_matrix_video(file_type,quality,values):
    if quality == "low_quality":
        quality_folder = "480p15"
    elif quality == "medium_quality":
        quality_folder = "720p30"
    elif quality == "high_quality":
        quality_folder = "1080p60"

    expected_filename = f"matrix_animation_{values}_{file_type}.mp4"

    video_file_path = linear_lab_videos_path(
        quality_folder,
        expected_filename,
    )

    if video_file_path.is_file():
        return str(video_file_path)
    else:
        return None