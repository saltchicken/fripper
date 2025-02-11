import tempfile
import os
import cv2
import subprocess
import platform
import signal
from .ffmpeg_cmd import rip_frames, grab_frame, seconds_to_hms, subtract_seconds, add_timestamps, get_clip, add_seconds


class VideoSplitter:
    def __init__(self, video_path, fps=4, start=None, nvidia=False):
        self.video_path = video_path
        self.fps = fps
        self.start = start
        self.nvidia = nvidia
        self.temp_dir = tempfile.TemporaryDirectory()
        self.frame_files = []
        self.total_frames = 0
        self.current_frame = 0
        self.start_timestamp = None
        self.end_timestamp = None
        self.rect_start_point = None
        self.rect_end_point = None
        self.drawing = False
        self.running = True

    def setup(self):
        rip_frames(self.video_path, self.temp_dir.name, "frame_%04d.jpg", fps=self.fps, start=self.start)
        self.frame_files = sorted(os.listdir(self.temp_dir.name))
        self.total_frames = len(self.frame_files)

        cv2.namedWindow("Frame Viewer", cv2.WINDOW_NORMAL)
        if platform.system() == "Linux":
            cv2.setWindowProperty("Frame Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.setMouseCallback("Frame Viewer", self.mouse_callback)
        cv2.createTrackbar("Frame", "Frame Viewer", 0, self.total_frames - 1, self.on_trackbar)
        self.show_frame(self.current_frame)

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.rect_start_point = (x, y)
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.rect_end_point = (x, y)
            self.show_frame(self.current_frame)
        elif event == cv2.EVENT_LBUTTONUP:
            self.rect_end_point = (x, y)
            self.drawing = False
            self.show_frame(self.current_frame)

    def show_frame(self, frame_index):
        if 0 <= frame_index < len(self.frame_files):
            frame_path = os.path.join(self.temp_dir.name, self.frame_files[frame_index])
            image = cv2.imread(frame_path)

            if self.rect_start_point and self.rect_end_point:
                cv2.rectangle(image, self.rect_start_point, self.rect_end_point, (0, 255, 0), 2)

            text = f"Frame: {frame_index + 1}/{self.total_frames}"
            image = cv2.putText(image, text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Frame Viewer", image)
        else:
            print("Invalid frame index.")

    def on_trackbar(self, val):
        self.current_frame = val
        self.show_frame(self.current_frame)

    def signal_handler(self, signum, frame):
        print("Interrupt received, exiting gracefully...")
        self.running = False

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        
        while self.running:
            key = cv2.waitKeyEx(1)
            if key == ord('q'):
                break
            elif key == 2424832:
                self.current_frame = max(self.current_frame - 1, 0)
            elif key == 2555904:
                self.current_frame = min(self.current_frame + 1, self.total_frames - 1)
            elif key == ord('s'):
                timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                if self.start:
                    timestamp = add_timestamps(timestamp, self.start)
                grab_frame(self.video_path, timestamp, crop=[self.rect_start_point, self.rect_end_point] if self.rect_start_point and self.rect_end_point else None)
            elif key == ord('['):
                self.start_timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                print(f"Start timestamp: {self.start_timestamp}")
            elif key == ord(']'):
                self.end_timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                print(f"End timestamp: {self.end_timestamp}")
            elif key == ord('c') and self.start_timestamp and self.end_timestamp:
                result = get_clip(self.video_path, self.start_timestamp, self.end_timestamp, crop=[self.rect_start_point, self.rect_end_point] if self.rect_start_point and self.rect_end_point else None)
                print(result)
            elif key == ord('o') and self.start_timestamp:
                for _ in range(20):
                    result = get_clip(self.video_path, self.start_timestamp, add_seconds(self.start_timestamp, 5))
                    print(result)
                    self.start_timestamp = add_seconds(self.start_timestamp, 4)
            elif key == ord(' '):
                timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                shifted_timestamp = subtract_seconds(timestamp, 1)
                subprocess.Popen(['fripper', 'split', self.video_path, "--fps", "60", "--start", shifted_timestamp])
            elif key == ord('d'):
                self.rect_start_point = None
                self.rect_end_point = None
                print("Crop box deleted")
            self.show_frame(self.current_frame)
            cv2.setTrackbarPos("Frame", "Frame Viewer", self.current_frame)
        cv2.destroyAllWindows()
        self.temp_dir.cleanup()


# Example Usage
# splitter = VideoSplitter("path/to/video.mp4", fps=4, start=None, nvidia=False)
# splitter.setup()
# splitter.run()

