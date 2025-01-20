import tempfile
import os
import cv2
from .ffmpeg_cmd import grab_frame
from .utils import seconds_to_hms


def preview_frame(video_path, start=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        image_path = grab_frame(video_path, start, temp_dir)
        print(image_path)

        # Initialize the OpenCV window
        cv2.namedWindow("Frame Viewer", cv2.WINDOW_NORMAL)


        image = cv2.imread(image_path)
        cv2.imshow("Frame Viewer", image)

        key = cv2.waitKey(0)

        if key == ord('q'):
            cv2.destroyAllWindows()

