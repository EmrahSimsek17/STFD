# Selected Three Frame Difference (STFD)

> **Selected Three Frame Difference Method for Moving Object Detection**

A lightweight moving object detection algorithm that improves the classical Three Frame Difference (TFD) method by selecting optimal image frames instead of using consecutive frames.

---

## Paper

**Selected Three Frame Difference Method for Moving Object Detection**

**Authors**

- Emrah Şimşek
- Barış Özyer

**Journal**

International Journal of Intelligent Systems and Applications in Engineering (IJISAE)

**Year**

2021


**Paper**

https://ijisae.org/index.php/IJISAE/article/view/1153

---

## Abstract

The classical Three Frame Difference (TFD) algorithm detects moving object edges by subtracting three consecutive image frames. Although computationally efficient, it generally produces incomplete foreground objects and therefore requires additional post-processing methods such as morphological operations or optical flow.

This study introduces the **Selected Three Frame Difference (STFD)** algorithm, which selects three non-overlapping frames according to the local maximum frame difference instead of using consecutive images. By applying logical operations to the selected frames, the proposed method is able to recover the complete moving object without any additional post-processing.

The proposed approach is mathematically analyzed and experimentally evaluated on both public benchmark datasets and real-world laboratory datasets.

---

## Motivation

Classical frame difference methods suffer from several limitations:

- Incomplete foreground objects
- Edge-only detection
- Fragmented moving regions
- Dependence on morphological operations
- Additional computational cost

STFD addresses these limitations by improving the frame selection strategy while preserving the simplicity and speed of frame differencing.

---

## Proposed Method

The proposed pipeline consists of the following steps:

```
Video Sequence
      │
      ▼
Frame Difference Analysis
      │
      ▼
Optimal Frame Selection
      │
      ▼
Selected Three Frames
      │
      ▼
Logical AND Operation
      │
      ▼
Moving Object Detection
```

Unlike the conventional TFD method,

```
Frame i
Frame i+1
Frame i+2
```

STFD selects

```
Frame A
Frame B
Frame C
```

where the selected frames maximize motion information while minimizing overlap between object positions.

---

## Key Contributions

- Novel frame selection strategy
- No morphological post-processing
- No optical flow computation
- Low computational complexity
- Complete moving object detection
- Suitable for real-time applications
- Easy integration into existing vision systems

---

## Advantages

Compared with the classical Three Frame Difference method:

- More complete foreground extraction
- Better object localization
- Reduced information loss
- Lower computational overhead
- Higher robustness for different motion speeds

---

## Applications

The proposed algorithm can be applied to:

- Intelligent surveillance
- Video analytics
- Traffic monitoring
- Wildlife monitoring
- Robotics
- UAV vision
- Smart cameras
- Embedded vision systems
- Edge AI applications

---

## Repository Structure

```
STFD
│
├── README.md
├── docs/
├── images/
├── examples/
├── videos/
├── datasets/
└── src/
```

---

## Future Improvements

Possible extensions include:

- GPU acceleration
- Adaptive threshold estimation
- Embedded implementation
- Multi-camera systems
- Moving camera adaptation
- Deep learning assisted STFD
- Event-based motion detection

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

This repository is intended for academic research and educational purposes.

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
