import subprocess
import tempfile
import os
import argparse

def main():
# Set up the argument parser
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")
    parser.add_argument("input_file", help="Path to the input video file")

# Parse the command-line arguments
    args = parser.parse_args()

# Input video file from command-line argument
    input_file = args.input_file

# Ensure the input file exists
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        exit(1)

# Create a temporary directory to store the frames
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define the output pattern for frame images (e.g., frame_0001.jpg, frame_0002.jpg, ...)
        output_pattern = os.path.join(temp_dir, "frame_%04d.jpg")
        
        # FFmpeg command to extract frames
        command = [
            "ffmpeg",
            "-i", input_file,    # Input video
            "-vf", "fps=1",      # Extract one frame per second
            output_pattern       # Output frames to temporary directory
        ]
        
        try:
            # Run the FFmpeg command to extract frames
            subprocess.run(command, check=True)
            print(f"Frames extracted to: {temp_dir}")
            
            # Example: Print the names of extracted frames
            for frame in os.listdir(temp_dir):
                print(f"Extracted frame: {frame}")
            
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
