import argparse
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def are_frames_duplicate_histogram(frame1, frame2, threshold=0.99999):
    hist1 = cv2.calcHist([frame1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([frame2], [0], None, [256], [0, 256])

    hist1 = cv2.normalize(hist1, hist1)
    hist2 = cv2.normalize(hist2, hist2)

    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity >= threshold

def are_frames_duplicate(frame1, frame2, threshold=0.99):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    similarity, _ = ssim(gray1, gray2, full=True)
    return similarity >= threshold

def filter_consecutive(lst, min_length=10):
    if not lst:
        return []

    lst.sort()
    filtered = []
    temp = [lst[0]]

    for i in range(1, len(lst)):
        if lst[i] == temp[-1] + 1:
            temp.append(lst[i])
        else:
            if len(temp) >= min_length:
                filtered.extend(temp)
            temp = [lst[i]]

    if len(temp) >= min_length:
        filtered.extend(temp)
    
    return filtered

def get_duplicate_frames(input_file):
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read the first frame.")
        return

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

    # print(f"Duplicate frames: {duplicates}")
    return duplicates

def remove_duplicate_frames(input_file, duplicate_frames):
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter('output.mkv', fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count not in duplicate_frames:
            out.write(frame)
        frame_count += 1

        # if frame_count in duplicates:
        #     cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count + 1)
        #     cap.set(cv2.CAP_PROP_POS_MSEC, 0)
        #     cap.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
        #     cap.set(cv2.CAP_PROP_POS_MSEC, 0
    cap.release()
    out.release()

def main():
    parser = argparse.ArgumentParser(description="Detect duplicate frames in a video.")
    parser.add_argument("input_file", type=str, help="Path to the video file")
    args = parser.parse_args()

    duplicate_frames = get_duplicate_frames(args.input_file)
    # print(duplicate_frames)
    filtered_duplicate_frames = filter_consecutive(duplicate_frames)
    # print(filtered_duplicate_frames)

    remove_duplicate_frames(args.input_file, filtered_duplicate_frames)



    

if __name__ == "__main__":
    main()
