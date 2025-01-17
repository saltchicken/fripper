import subprocess
import tempfile
import os
import argparse
import cv2

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
        
        # FFmpeg command to extract frames 4 times per second
        command = [
            "ffmpeg",
            "-i", input_file,    # Input video
            "-vf", "fps=4",      # Extract 4 frames per second
            output_pattern       # Output frames to temporary directory
        ]
        
        try:
            # Run the FFmpeg command to extract frames
            subprocess.run(command, check=True)
            print(f"Frames extracted to: {temp_dir}")
            
            # List all extracted frame images
            frame_files = sorted(os.listdir(temp_dir))
            total_frames = len(frame_files)
            
            # Initialize the OpenCV window
            cv2.namedWindow("Frame Viewer", cv2.WINDOW_NORMAL)
            
            # Function to convert seconds to HH:MM:SS format
            def seconds_to_hms(seconds):
                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                secs = seconds % 60
                return f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"  # Include milliseconds

            # Function to display the current frame with frame number and total frames overlay
            def show_frame(frame_index):
                if 0 <= frame_index < len(frame_files):
                    frame_path = os.path.join(temp_dir, frame_files[frame_index])
                    image = cv2.imread(frame_path)

                    # Overlay the current frame number and total frames on the image
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = f"Frame: {frame_index + 1}/{total_frames}"
                    color = (0, 255, 0)  # Green color
                    thickness = 2
                    position = (30, 30)  # Position to place the text
                    image = cv2.putText(image, text, position, font, 1, color, thickness, lineType=cv2.LINE_AA)
                    
                    cv2.imshow("Frame Viewer", image)
                else:
                    print("Invalid frame index.")
            
            # Show the first frame
            current_frame = 0
            show_frame(current_frame)
            
            # Create a trackbar (slider) to control the frame navigation
            def on_trackbar(val):
                nonlocal current_frame
                current_frame = val
                show_frame(current_frame)

            cv2.createTrackbar("Frame", "Frame Viewer", 0, total_frames - 1, on_trackbar)
            
            while True:
                # Wait for user input
                key = cv2.waitKeyEx(1)  # 1 means wait for 1 ms, allowing slider movement
                
                if key == ord('q'):  # Press 'q' to quit
                    break
                elif key == 2424832:  # Left arrow key (OpenCV key code)
                    current_frame = max(current_frame - 1, 0)  # Move 1 frame backward
                    show_frame(current_frame)
                    cv2.setTrackbarPos("Frame", "Frame Viewer", current_frame)  # Update slider
                elif key == 2555904:  # Right arrow key (OpenCV key code)
                    current_frame = min(current_frame + 1, len(frame_files) - 1)  # Move 1 frame forward
                    show_frame(current_frame)
                    cv2.setTrackbarPos("Frame", "Frame Viewer", current_frame)  # Update slider
                elif key == ord(' '):  # Spacebar to print the current frame's timestamp
                    timestamp = seconds_to_hms(current_frame / 4)  # Divide by 4 since there are 4 frames per second
                    print(f"Current frame timestamp (FFmpeg format): {timestamp}")
            
            # Close the OpenCV window
            cv2.destroyAllWindows()

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

