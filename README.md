# Selected Three Frame Difference (STFD) for Moving Object Detection

Official Python implementation of the paper:

> **Selected Three Frame Difference Method for Moving Object Detection**  
> Emrah Simsek, Baris Ozyer  
> *International Journal of Intelligent Systems and Applications in Engineering (IJISAE)*, 2021, 9(2), 48–54  
> **Paper** https://ijisae.org/index.php/IJISAE/article/view/1153

---

## Overview

Classic Three Frame Difference (TFD) detects only the **edges** of moving objects
because the method applies a logical AND between two consecutive frame differences,
leaving holes inside foreground regions.

STFD solves this by **selecting** the three frames intelligently:

1. **Id1** – first frame where motion is detected.  
2. **Id2** – frame at the first local maximum of cumulative intensity change from Id1.  
3. **Id3** – frame at the next local maximum measured from Id2.

Because the selected frames contain **non-overlapping** object positions, the
logical AND of their differences always yields the **complete** object region in Id2
(mathematically proved in the paper).

```
Image Sequence  →  Local-Max Selection  →  Frame Difference  →  Logical AND  →  Full Object Mask
                        (Algorithm 1 & 2)        (If1, If2)          (Ib)
```

---

## Repository Structure

```
STFD/
├── stfd.py              # Core STFD class (import this in your own project)
├── run_detection.py     # CLI script to run on any video file
├── requirements.txt
├── examples/
│   └── basic_usage.py   # Minimal usage example
└── README.md
```

---

## Installation

```bash
git clone https://github.com/EmrahSimsek17/STFD.git
cd STFD
pip install -r requirements.txt
```

Requires Python ≥ 3.7.

---

## Quick Start

### Command-line

```bash
# Live preview
python run_detection.py --input Walk3.mpg

# Save output video
python run_detection.py --input Walk3.mpg --output result.mp4

# Headless (no window) with custom threshold
python run_detection.py --input video.mp4 --threshold 20 --no-display --output out.mp4
```

### Python API

```python
import cv2
from stfd import STFD

cap = cv2.VideoCapture("Walk3.mpg")
detector = STFD(threshold=17)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    annotated, detections = detector.detect(frame)
    # detections → list of (x_min, y_min, x_max, y_max)

    cv2.imshow("STFD", annotated)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## Parameters

| Parameter | Default | Description |
|---|---|---|
| `threshold` | `17` | Global binary threshold applied to frame difference images. |
| `median_ratio` | `0.02` (1/50) | Median filter kernel size as a fraction of frame width. |
| `min_object_ratio` | `700` | Minimum object area filter: components smaller than `frame_area / ratio` are discarded. |

---

## Algorithm Details

### Stage 1 – Frame Selection (Algorithms 1 & 2)

For each incoming frame `k+i`, the total intensity change `D_i` relative to the
selected reference frame `Id1` is computed:

```
D_i = Σ Σ I_fi(x, y)
```

While `D_{i+1} − D_i ≥ 0` the difference is still growing (object regions still separating).
The moment the difference **decreases** (`< 0`) a **local maximum LM_j** is declared
and the corresponding binary image is stored as the second selected frame Id2.
The process repeats from Id2 to find Id3.

### Stage 2 – Detection (Equation 7)

```
Of1 ∩ Of2 = (Od1 ∪ Od2) ∩ (Od2 ∪ Od3)
           = Od2          (since Od1 ∩ Od2 = Od2 ∩ Od3 = ∅)
```

The AND of the two difference images isolates `Od2` — the complete object at Id2.

### Stage 3 – Connected Component Analysis (Algorithm 3)

Small noise regions are removed based on their relative area. Bounding boxes are
drawn around surviving components.

---

## Benchmark Results

| Video | Precision | Recall | F-Score |
|---|---|---|---|
| Caviar Walk1 | 0.98 | 0.97 | **0.97** |
| Caviar Walk2 | 0.72 | 0.93 | **0.81** |
| Caviar Walk3 | 0.98 | 0.83 | **0.90** |
| FMO frisbee  | 1.00 | 1.00 | **1.00** |
| CTRIN Video1 | 0.99 | 0.98 | **0.98** |

Full comparison with TFD and eight background-subtraction baselines (MOG, GMG, MOG2,
GRA, CNT, GSOC, KNN, LSBP) is available in the paper.

---

## Datasets

- [CAVIAR](https://groups.inf.ed.ac.uk/vision/CAVIAR/CAVIARDATA1/)
- [Fast Moving Object (FMO)](http://cmp.felk.cvut.cz/fmo/)
- [LASIESTA](https://www.gti.ssr.upm.es/data/lasiesta_database.html)
- [CTRIN (our lab dataset)](http://cogvi.atauni.edu.tr/ResearchLab/PageDetail/Our-CTRIN-Dataset-87)

---

## License

This project is licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) License.

---

## Citation

If you use this work, please cite:

```bibtex
@article{Simsek2021STFD,
  author = {Emrah Şimşek and Barış Özyer},
  title = {Selected Three Frame Difference Method for Moving Object Detection},
  journal = {International Journal of Intelligent Systems and Applications in Engineering},
  volume = {9},
  number = {2},
  pages = {48--54},
  year = {2021},
  doi = {10.18201/ijisae.2021.233}
}
```

---

## Related Research

This work forms the basis for several subsequent studies on moving object detection, including:

- Pattern recognition-assisted motion detection
- Semantic moving object detection
- Training-free moving object detection
- Moving object detection using semantic cues
- Edge AI-based real-time perception systems

---

## License

Copyright (c) 2026 Emrah Şimşek

This software is provided solely for academic, educational and research purposes.

Commercial use, redistribution within commercial products,
or incorporation into proprietary software is prohibited
without prior written permission from the copyright holder.

For commercial licensing inquiries, please contact:

emrah.simsek@erzurum.edu.tr

---

Notice

The documentation, explanations, and source code in this repository have been reviewed and enhanced with the assistance of artificial intelligence to improve clarity, consistency, and readability.

If you encounter any errors, inaccuracies, or have suggestions for improvement, please feel free to contact me at:

📧 emrah.simsek@erzurum.edu.tr

Your feedback is greatly appreciated and will help improve the quality of this repository.

---

## Author

**Dr. Emrah Şimşek**

Research Interests

- Computer Vision
- Moving Object Detection
- Embedded AI
- Edge AI
- Visual Odometry
- Autonomous Systems
