import tempfile
import os
import cv2
import subprocess
import platform
import signal
import threading
import imghdr
import shutil
from PIL import Image
from .ffmpeg_cmd import rip_frames, grab_frame, seconds_to_hms, subtract_seconds, add_timestamps, get_clip, add_seconds

def is_image(file_path):
    return imghdr.what(file_path) is not None

def crop_image(image_path, top_left, bottom_right):
    img = Image.open(image_path)

    crop_box = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

    cropped_img = img.crop(crop_box)
    basename = os.path.splitext(os.path.basename(image_path))[0]

    cropped_img.save(basename + "_cropped.png")  # Save the cropped image

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
        if not is_image(self.video_path):
            print("its a video")
            rip_frames(self.video_path, self.temp_dir.name, "frame_%05d.jpg", fps=self.fps, start=self.start)
        else:
            print("Its an image")
            try:
                shutil.copy(self.video_path, self.temp_dir.name)
                print("Image file opened")
            except Exception as e:
                print(f"Error occurred: {e}")

        self.frame_files = sorted(os.listdir(self.temp_dir.name))
        self.total_frames = len(self.frame_files)
        if is_image(self.video_path):
            self.total_frames = 2

        cv2.namedWindow("Frame Viewer", cv2.WINDOW_NORMAL)
        if platform.system() == "Linux":
            cv2.setWindowProperty("Frame Viewer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        cv2.setMouseCallback("Frame Viewer", self.mouse_callback)
        cv2.createTrackbar("Frame", "Frame Viewer", 0, self.total_frames - 1, self.on_trackbar)
        self.show_frame(self.current_frame)

    def mouse_callback(self, event, x, y, flags, param):
        shift_held = flags & cv2.EVENT_FLAG_SHIFTKEY  # Check if Shift is held
        if event == cv2.EVENT_LBUTTONDOWN:
            self.rect_start_point = (x, y)
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            if shift_held:
                self.rect_end_point = (self.rect_start_point[0] + 512, self.rect_start_point[1] + 512)
            else:
                self.rect_end_point = (x, y)
            self.show_frame(self.current_frame)
        elif event == cv2.EVENT_LBUTTONUP:
            if shift_held:
                x = self.rect_start_point[0] + 512
                y = self.rect_start_point[1] + 512
            if x > self.width:
                x = self.width
            elif x < 0:
                x = 0
            if y > self.height:
                y = self.height
            elif y < 0:
                y = 0

            x1, y1 = self.rect_start_point
            x2, y2 = x, y

            self.rect_start_point = (min(x1, x2), min(y1, y2))
            self.rect_end_point = (max(x1, x2), max(y1, y2))
            self.drawing = False
            print(f"{self.rect_start_point} {self.rect_end_point}")
            self.show_frame(self.current_frame)

    def show_frame(self, frame_index):
        if 0 <= frame_index < len(self.frame_files):
            frame_path = os.path.join(self.temp_dir.name, self.frame_files[frame_index])
            image = cv2.imread(frame_path)
            self.height, self.width = image.shape[:2]

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
                if not is_image(self.video_path):
                    timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                    if self.start:
                        timestamp = add_timestamps(timestamp, self.start)
                    grab_frame(self.video_path, timestamp, crop=[self.rect_start_point, self.rect_end_point] if self.rect_start_point and self.rect_end_point else None)
                else:
                    if self.rect_start_point and self.rect_end_point:
                        crop_image(self.video_path, self.rect_start_point, self.rect_end_point)
                    else:
                        print("No crop box for image, skipping")


            elif key == ord('['):
                self.start_timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                print(f"Start timestamp: {self.start_timestamp}")
            elif key == ord(']'):
                self.end_timestamp = seconds_to_hms(self.current_frame / int(self.fps))
                print(f"End timestamp: {self.end_timestamp}")
            elif key == ord('c') and self.start_timestamp and self.end_timestamp:
                def extract_clip():
                    result = get_clip(self.video_path, self.start_timestamp, self.end_timestamp, 
                                    crop=[self.rect_start_point, self.rect_end_point] if self.rect_start_point and self.rect_end_point else None)
                    print(result)

                threading.Thread(target=extract_clip, daemon=True).start()

                # result = get_clip(self.video_path, self.start_timestamp, self.end_timestamp, crop=[self.rect_start_point, self.rect_end_point] if self.rect_start_point and self.rect_end_point else None)
                # print(result)
            elif key == ord('t') and self.start_timestamp:
                def extract_clip():
                    result = get_frame_count(self.video_path, self.start_timestamp, 33, fps=16, crop=[self.rect_start_point, self.rect_end_point] if self.rect_start_point and self.rect_end_point else None)

                    print(result)
                threading.Thread(target=extract_clip, daemon=True).start()
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

