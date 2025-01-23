import tempfile
import os
import cv2
from .ffmpeg_cmd import grab_frame, grab_thumbnails, seconds_to_hms, calculate_inner_thumbnail_positions


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

def preview_thumbnails(video_path):
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = grab_thumbnails(video_path, temp_dir)
        images = [cv2.imread(path) for path in image_paths]
        width, height = images[0].shape[1], images[0].shape[0]
        width = width // 2
        height = height // 2
        resized_images = [cv2.resize(image, (width, height)) for image in images]

        top_row = cv2.hconcat(resized_images[:2])
        bottom_row = cv2.hconcat(resized_images[2:])

        stitched_image = cv2.vconcat([top_row, bottom_row])
        cv2.imshow('Stitched Image', stitched_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


