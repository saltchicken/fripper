import os
import subprocess


def is_path_valid(video_path):
    """
    Checks if the specified video file path exists. If the file does not exist,
    a FileNotFoundError is raised.

    Args:
        video_path (str): The path to the video file to check for existence.

    Returns:
        None

    Raises:
            FileNotFoundError: If the video file does not exist.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Error: The file '{video_path}' does not exist")


def rip_frames(video_path, output_directory, output_pattern, fps=4, nvidia=False):
    """
    Extracts frames from a video file using FFmpeg and saves them to the specified
    output directory a specified frame rate.

    Optionally, NVIDIA CUDA hardware acceleration can be used for faster frame extraction.

    Args:
        video_path (str): The path to the input video file to extract frames from.
        output_directory (str): The directory where the extracted frames will be saved.
        output_pattern (str): The filename pattern for the output frames
                            (e.g., 'frame_%04d.jpg' for sequentially numbered frames).
        fps (int, optional): The frame rate (frames per second) at which to extract frames.
                             Defaults to 4.
        nvidia (bool, optional): Whether to use NVIDIA CUDA hardware acceleration for
                            processing. Defaults to False.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input video file does not exist (checked via `is_path_valid`).
        subprocess.CalledProcessError: If FFmpeg encounters an error during execution.
        Exception: For any other unexpected errors.

    Example:
        >>> rip_frames("video.mp4", "output_frames", "frame_%04d.jpg", fps=5)
        Frames extracted to: output_frames

    Notes:
        - Ensure FFmpeg is installed and accessible from the system's PATH.
    """

    is_path_valid(video_path)
    output_pattern = os.path.join(output_directory, output_pattern)

    if nvidia:
        command = [
            "ffmpeg",
            "-hwaccel",
            "cuda",
            "-i",
            video_path,  # Input video
            "-vf",
            f"fps={fps}",  # Extract 4 frames per second
            output_pattern,  # Output frames to temporary directory
        ]
    else:
        command = [
            "ffmpeg",
            "-i",
            video_path,  # Input video
            "-vf",
            f"fps={fps}",  # Extract 4 frames per second
            output_pattern,  # Output frames to temporary directory
        ]

    try:
        # Run the FFmpeg command to extract frames
        subprocess.run(command, check=True)
        print(f"Frames extracted to: {output_directory}")

    except subprocess.CalledProcessError as e:
        print(f"FFmpeg subprocess failure: {e}")
        raise subprocess.CalledProcessError

def grab_frame(video_path, timestamp, output_directory=None):
    # TODO: Validate timestamp
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    timestamp_str = timestamp.replace(":", "-").replace(".", "-")

    if output_directory:
        is_path_valid(output_directory)
        output_image_path = os.path.join(output_directory, f"{video_filename}_{timestamp_str}.jpg")
    else:
        output_image_path = os.path.join(os.getcwd(), f"{video_filename}_{timestamp_str}.jpg")

    command = [
            "ffmpeg",
            "-ss", timestamp,  # Seek to the specific timestamp
            "-i", video_path,  # Input video
            "-frames:v", "1",  # Extract only one frame
            "-q:v", "2",       # Set quality (lower value = higher quality)
            output_image_path, # Output image path
            "-y"               # Overwrite output file if it exists
        ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Frame extracted and saved to {output_image_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")



