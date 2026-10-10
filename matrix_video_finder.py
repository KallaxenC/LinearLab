from pathlib import Path

def find_matrix_video(a, b, c, d):
    # Construct the expected filename based on the matrix values
    expected_filename = f"matrix_animation_{a}{b}{c}{d}.mp4"

    script_dir = Path(__file__).resolve().parent
    # Create a Path object for the output folder
    #output_path = Path(output_folder)
    video_file_path = script_dir / "media" / "videos" / "720p30" / expected_filename

    if video_file_path.exists():
        return str(video_file_path)
    else:
        return None