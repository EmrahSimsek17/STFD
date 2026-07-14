"""
examples/basic_usage.py
-----------------------
Minimal example showing how to use the STFD class programmatically.
"""

import cv2
from stfd import STFD   # make sure the parent directory is on sys.path


def run(video_path: str):
    cap = cv2.VideoCapture(video_path)
    detector = STFD(threshold=17)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        annotated, detections = detector.detect(frame)

        # detections → list of (x_min, y_min, x_max, y_max) tuples
        for (x1, y1, x2, y2) in detections:
            print(f"  Object at ({x1},{y1}) → ({x2},{y2})")

        cv2.imshow("STFD", annotated)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    video = sys.argv[1] if len(sys.argv) > 1 else "Walk3.mpg"
    run(video)
