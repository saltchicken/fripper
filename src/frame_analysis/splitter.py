import subprocess
import tempfile
import os
import sys
import cv2


def splitter(video_path, fps=4, nvidia=False):
    # Ensure the input file exists
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        sys.exit(1)

    # Create a temporary directory to store the frames
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define the output pattern for frame images (e.g., frame_0001.jpg,
        # frame_0002.jpg, ...)
        output_pattern = os.path.join(temp_dir, "frame_%04d.jpg")

        # FFmpeg command to extract frames 4 times per second
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
                # Include milliseconds
                return f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

            # Function to display the current frame with frame number and total frames overlay
            def show_frame(frame_index):
                if 0 <= frame_index < len(frame_files):
                    frame_path = os.path.join(
                        temp_dir, frame_files[frame_index])
                    image = cv2.imread(frame_path)

                    # Overlay the current frame number and total frames on the image
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    text = f"Frame: {frame_index + 1}/{total_frames}"
                    color = (0, 255, 0)  # Green color
                    thickness = 2
                    position = (30, 30)  # Position to place the text
                    image = cv2.putText(
                        image, text, position, font, 1, color, thickness, lineType=cv2.LINE_AA)

                    cv2.imshow("Frame Viewer", image)
                else:
                    print("Invalid frame index.")

            current_frame = 0
            show_frame(current_frame)

            def on_trackbar(val):
                nonlocal current_frame
                current_frame = val
                show_frame(current_frame)

            cv2.createTrackbar("Frame", "Frame Viewer", 0,
                               total_frames - 1, on_trackbar)

            while True:
                key = cv2.waitKeyEx(1)

                if key == ord('q'):
                    break
                if key == 2424832:
                    current_frame = max(current_frame - 1, 0)
                    show_frame(current_frame)
                    cv2.setTrackbarPos("Frame", "Frame Viewer",
                                       current_frame)  # Update slider
                elif key == 2555904:
                    current_frame = min(current_frame + 1,
                                        len(frame_files) - 1)
                    show_frame(current_frame)
                    cv2.setTrackbarPos("Frame", "Frame Viewer", current_frame)
                elif key == ord(' '):
                    timestamp = seconds_to_hms(current_frame / 4)
                    print(f"Current frame timestamp (FFmpeg format): {timestamp}")

            # Close the OpenCV window
            cv2.destroyAllWindows()

        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
