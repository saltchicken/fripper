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
            
            # List all extracted frame images
            frame_files = sorted(os.listdir(temp_dir))
            
            # Initialize the OpenCV window
            cv2.namedWindow("Frame Viewer", cv2.WINDOW_NORMAL)
            
            # Track the current frame index
            current_frame = 0
            
            # Function to display the current frame with frame number overlay
            def show_frame(frame_index):
                if 0 <= frame_index < len(frame_files):
                    frame_path = os.path.join(temp_dir, frame_files[frame_index])
                    image = cv2.imread(frame_path)

                    # Overlay the current frame number on the image
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = f"Frame: {frame_index + 1}"
                    color = (0, 255, 0)  # Green color
                    thickness = 2
                    position = (30, 30)  # Position to place the text
                    image = cv2.putText(image, text, position, font, 1, color, thickness, lineType=cv2.LINE_AA)
                    
                    cv2.imshow("Frame Viewer", image)
                else:
                    print("Invalid frame index.")
            
            # Show the first frame
            show_frame(current_frame)
            
            while True:
                # Wait for user input to navigate frames
                key = cv2.waitKeyEx(0)  # 0 means wait indefinitely for a key press
                
                if key == ord('q'):  # Press 'q' to quit
                    break
                elif key == 2424832:  # Left arrow key (OpenCV key code)
                    current_frame = max(current_frame - 1, 0)
                    show_frame(current_frame)
                elif key == 2555904:  # Right arrow key (OpenCV key code)
                    current_frame = min(current_frame + 1, len(frame_files) - 1)
                    show_frame(current_frame)
            
            # Close the OpenCV window
            cv2.destroyAllWindows()

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

