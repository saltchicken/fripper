import subprocess
import os
import sys


def is_path_valid(video_path):
    """
    Checks if the specified video file path exists. If the file does not exist,
    an error message is printed and the program exits with a status code of 1.

    Args:
        video_path (str): The path to the video file to check for existence.

    Returns:
        None

    Exits:
        The program exits with status code 1 if the video file does not exist.
    """
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        sys.exit(1)


def rip_frames(video_path, output_directory, output_pattern, fps=4, nvidia=False):
    is_path_valid(video_path)
    output_pattern = os.path.join(output_directory, output_pattern)

    if nvidia:
        command = [
            "ffmpeg",
            "-hwaccel", "cuda",
            "-i", video_path,    # Input video
            "-vf", f"fps={fps}",      # Extract 4 frames per second
            output_pattern       # Output frames to temporary directory
        ]
    else:
        command = [
            "ffmpeg",
            "-i", video_path,    # Input video
            "-vf", f"fps={fps}",      # Extract 4 frames per second
            output_pattern       # Output frames to temporary directory
        ]

    try:
        # Run the FFmpeg command to extract frames
        subprocess.run(command, check=True)
        print(f"Frames extracted to: {output_directory}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
