"""
run_detection.py – Run STFD moving-object detection on a video file.

Usage
-----
    python run_detection.py --input Walk3.mpg
    python run_detection.py --input Walk3.mpg --output result.mp4 --threshold 17
    python run_detection.py --input Walk3.mpg --no-display --output result.mp4

Press  q  to quit the live preview window.
"""

import argparse
import sys

import cv2

from stfd import STFD


def parse_args():
    parser = argparse.ArgumentParser(
        description="Selected Three Frame Difference (STFD) Moving Object Detector"
    )
    parser.add_argument("--input", required=True,
                        help="Path to input video file or camera index (e.g. 0).")
    parser.add_argument("--output", default=None,
                        help="Optional path to save annotated output video (.mp4).")
    parser.add_argument("--threshold", type=int, default=17,
                        help="Binary threshold value (default: 17).")
    parser.add_argument("--median-ratio", type=float, default=0.02,
                        help="Median kernel as fraction of frame width (default: 0.02 = 1/50).")
    parser.add_argument("--min-object-ratio", type=float, default=700,
                        help="Minimum object size filter: frame_area / ratio (default: 700).")
    parser.add_argument("--no-display", action="store_true",
                        help="Disable live preview window (useful for headless servers).")
    return parser.parse_args()


def open_capture(source: str):
    """Open a VideoCapture from a file path or camera index."""
    try:
        src = int(source)
    except ValueError:
        src = source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open video source: {source}")
        sys.exit(1)
    return cap


def make_writer(cap: cv2.VideoCapture, output_path: str):
    """Create a VideoWriter with the same fps/size as the capture."""
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    return cv2.VideoWriter(output_path, fourcc, fps, (w, h))


def main():
    args = parse_args()

    cap = open_capture(args.input)
    writer = make_writer(cap, args.output) if args.output else None

    detector = STFD(
        threshold=args.threshold,
        median_ratio=args.median_ratio,
        min_object_ratio=args.min_object_ratio,
    )

    frame_idx = 0
    print("[INFO] Processing video… (press 'q' to quit)")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        annotated, detections = detector.detect(frame)

        if detections:
            print(f"  Frame {frame_idx:5d}: {len(detections)} object(s) detected")

        if writer:
            writer.write(annotated)

        if not args.no_display:
            cv2.imshow("STFD – Moving Object Detection", annotated)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        frame_idx += 1

    cap.release()
    if writer:
        writer.release()
        print(f"[INFO] Saved output video to: {args.output}")
    cv2.destroyAllWindows()
    print(f"[INFO] Done. Processed {frame_idx} frames.")


if __name__ == "__main__":
    main()
