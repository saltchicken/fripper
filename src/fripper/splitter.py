import tempfile
import os
import cv2
import subprocess
from .ffmpeg_cmd import rip_frames, grab_frame, seconds_to_hms, subtract_seconds, add_timestamps, get_clip

start_timestamp = None
end_timestamp = None

def splitter(video_path, fps=4, start=None, nvidia=False):
    with tempfile.TemporaryDirectory() as temp_dir:
        rip_frames(video_path, temp_dir, "frame_%04d.jpg", fps=fps, start=start)

        # List all extracted frame images
        frame_files = sorted(os.listdir(temp_dir))
        total_frames = len(frame_files)

        # Initialize the OpenCV window
        cv2.namedWindow("Frame Viewer", cv2.WINDOW_NORMAL)


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
            elif key == ord('s'):
                timestamp = seconds_to_hms(current_frame / int(fps)) 
                if start:
                    timestamp = add_timestamps(timestamp, start)
                grab_frame(video_path, timestamp)
            elif key == ord('['):
                start_timestamp = seconds_to_hms(current_frame / int(fps)) 
            elif key == ord(']'):
                end_timestamp = seconds_to_hms(current_frame / int(fps))
            elif key == ord('c'):
                # TODO: Add check to see if end_timestamp is greater than start_timestamp
                if start_timestamp and end_timestamp:
                    result = get_clip(video_path, start_timestamp, end_timestamp)
                    print(result)
                else:
                    print("Please select a starting and ending timestamp using the '[' and ']' keys.")

            elif key == ord(' '):
                timestamp = seconds_to_hms(current_frame / int(fps))
                print(f"Current frame timestamp (FFmpeg format): {timestamp}")

                #TODO: Hacky solution
                shifted_timestamp = subtract_seconds(timestamp, 1)
                subprocess.Popen(['frame_analysis', 'split', video_path, "--fps", "60", "--start", shifted_timestamp])

        # Close the OpenCV window
        cv2.destroyAllWindows()
