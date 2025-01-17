import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Extract a frame from a video at a specific timestamp using FFmpeg.")
    parser.add_argument("video_path", help="Path to the input video file.")
    parser.add_argument("timestamp", help="Timestamp to extract the frame (format: HH:MM:SS.mmm).")
    parser.add_argument("output_image_path", help="Path to save the extracted frame (e.g., frame.jpg).")
    
    args = parser.parse_args()
    
    extract_frame(args.video_path, args.timestamp, args.output_image_path)


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

if __name__ == "__main__":
    main()

