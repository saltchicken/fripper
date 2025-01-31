import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def are_frames_duplicate_histogram(frame1, frame2, threshold=0.99999):
    hist1 = cv2.calcHist([frame1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([frame2], [0], None, [256], [0, 256])

    # Normalize histograms
    hist1 = cv2.normalize(hist1, hist1)
    hist2 = cv2.normalize(hist2, hist2)

    # Compare histograms using correlation
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity >= threshold

def are_frames_duplicate(frame1, frame2, threshold=0.99):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM
    similarity, _ = ssim(gray1, gray2, full=True)

    return similarity >= threshold

# Open video file
cap = cv2.VideoCapture("C:/Users/saltchicken/Desktop/test.mkv")

ret, prev_frame = cap.read()
frame_count = 0
duplicates = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if are_frames_duplicate_histogram(prev_frame, frame):
        duplicates.append(frame_count)

    prev_frame = frame
    frame_count += 1

cap.release()

print(f"Duplicate frames: {duplicates}")
