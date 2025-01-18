import subprocess
import argparse
import os

def grabber(video_path, timestamp):

    # Generate unique output image path based on timestamp
    output_image_path = generate_unique_image_path(video_path, timestamp)
    
    extract_frame(video_path, timestamp, output_image_path)


def extract_frame(video_path, timestamp, output_image_path):
    """
    Extracts a frame from a video at a specific timestamp.

    :param video_path: Path to the input video file.
    :param timestamp: The timestamp to extract the frame (format: HH:MM:SS.mmm).
    :param output_image_path: Path to save the extracted frame (e.g., frame.jpg).
    """
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


def generate_unique_image_path(video_path, timestamp):
    """
    Generate a unique image path based on the video filename and timestamp.

    :param video_path: Path to the input video file.
    :param timestamp: The timestamp to extract the frame (format: HH:MM:SS.mmm).
    :return: A unique file path for the output image.
    """
    # Extract the base video filename without extension
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    
    # Format the timestamp to a filename-friendly format (replace colons and periods with underscores)
    timestamp_str = timestamp.replace(":", "-").replace(".", "-")
    
    # Create a unique output path
    output_dir = os.path.dirname(video_path)  # Save in the same directory as the video
    output_image_path = os.path.join(output_dir, f"{video_filename}_{timestamp_str}.jpg")
    
    return output_image_path


if __name__ == "__main__":
    main()

