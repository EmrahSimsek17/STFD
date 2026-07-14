"""
Selected Three Frame Difference (STFD) Method for Moving Object Detection
==========================================================================
Implementation of the paper:
    "Selected Three Frame Difference Method for Moving Object Detection"
    Emrah Simsek, Baris Ozyer
    International Journal of Intelligent Systems and Applications in Engineering
    IJISAE, 2021, 9(2), 48-54

Algorithm Overview:
    1. Select first reference frame (Id1) when motion is detected.
    2. Find second frame (Id2) at the local maximum of intensity changes from Id1.
    3. Find third frame (Id3) at the next local maximum from Id2.
    4. Apply logical AND between frame difference outputs (If1, If2) to isolate
       the complete moving object region in the second selected frame.
"""

import cv2
import numpy as np


class STFD:
    """
    Selected Three Frame Difference detector.

    Parameters
    ----------
    threshold : int
        Binary threshold value (default: 17).
    median_ratio : float
        Ratio of frame width used to compute median filter kernel size (default: 1/50).
    min_object_ratio : float
        Connected component size must exceed (frame_area / min_object_ratio)
        to be kept as a valid detection (default: 700, equivalent to 1/700
        of the total frame area).
    """

    def __init__(self, threshold: int = 17, median_ratio: float = 1 / 50,
                 min_object_ratio: float = 700):
        self.threshold = threshold
        self.median_ratio = median_ratio
        self.min_object_ratio = min_object_ratio

        # Internal state
        self._stage = 0          # 0: waiting, 1: collecting, 2: detecting
        self._ref_frame = None   # Id1 – selected first image
        self._outputs = []       # accumulated frame-difference binaries
        self._prev_total = 0     # D_{i-1} for local-maximum search
        self._best_diff = None   # frame diff at current local max
        self._ker = None         # median filter kernel size (computed once)

        # Intermediate results kept for Phase 2
        self._sonuc_1 = None     # If1 minus AND mask (complement region)
        self._sonuc_2 = None     # AND mask (intersection of outputs[0] & outputs[1])

        self._frame_h = None
        self._frame_w = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def detect(self, frame_bgr: np.ndarray):
        """
        Process a single BGR frame and return annotated frame with bounding boxes.

        Parameters
        ----------
        frame_bgr : np.ndarray
            Input frame in BGR colour space (as returned by cv2.VideoCapture.read).

        Returns
        -------
        annotated : np.ndarray
            Copy of input frame with cyan bounding boxes drawn around detected objects.
        detections : list[tuple[int,int,int,int]]
            List of (x_min, y_min, x_max, y_max) bounding boxes.
        """
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        annotated = frame_bgr.copy()
        detections = []

        # Compute kernel size once
        if self._ker is None:
            self._frame_h, self._frame_w = gray.shape
            ker = int(self._frame_w * self.median_ratio)
            self._ker = ker + 1 if ker % 2 == 0 else ker

        if self._stage == 0:
            # Stage 0: store first reference frame
            self._ref_frame = gray
            self._stage = 1

        elif self._stage == 1:
            # Stage 1: hunt for the two local-maximum frames
            diff_img = self._compute_diff(self._ref_frame, gray)
            total = int(diff_img.sum())

            if total - self._prev_total >= 0:
                # Still climbing → keep tracking
                self._prev_total = total
                self._best_diff = diff_img
            else:
                # Passed a local maximum → record it
                self._prev_total = 0
                self._outputs.append(self._best_diff)

                if len(self._outputs) == 2:
                    # Both local-max frames collected → build masks
                    and_mask = cv2.bitwise_and(self._outputs[0], self._outputs[1])
                    self._sonuc_2 = and_mask
                    self._sonuc_1 = cv2.absdiff(self._outputs[0], and_mask)
                    self._stage = 2

        else:
            # Stage 2: continuous detection
            diff_img = self._compute_diff(self._ref_frame, gray)
            result = cv2.absdiff(diff_img, self._sonuc_1)
            result = cv2.medianBlur(result, self._ker)

            detections, annotated = self._extract_boxes(result, frame_bgr)

        return annotated, detections

    def reset(self):
        """Reset detector state (e.g. after a scene cut)."""
        self.__init__(self.threshold, self.median_ratio, self.min_object_ratio)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _compute_diff(self, frame_a: np.ndarray, frame_b: np.ndarray) -> np.ndarray:
        """Absolute difference → median filter → binary threshold."""
        diff = cv2.absdiff(frame_a, frame_b)
        diff = cv2.medianBlur(diff, self._ker)
        _, diff = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
        diff = cv2.medianBlur(diff, self._ker)
        return diff

    def _extract_boxes(self, binary: np.ndarray, frame_bgr: np.ndarray):
        """
        Run connected-component analysis and draw bounding boxes.

        Components whose area is less than (frame_area / min_object_ratio)
        are discarded as noise (Algorithm 3 in the paper).
        """
        annotated = frame_bgr.copy()
        detections = []

        frame_area = self._frame_h * self._frame_w
        n_labels, labels = cv2.connectedComponents(binary)
        thickness = max(1, int(self._frame_w / 150))

        for label in range(1, n_labels):
            coords = np.argwhere(labels == label)
            if frame_area / len(coords) >= self.min_object_ratio:
                continue  # too small → skip

            y_min, x_min = coords.min(axis=0)
            y_max, x_max = coords.max(axis=0)
            detections.append((int(x_min), int(y_min), int(x_max), int(y_max)))
            cv2.rectangle(annotated, (x_min, y_min), (x_max, y_max),
                          (255, 255, 0), thickness)

        return detections, annotated
