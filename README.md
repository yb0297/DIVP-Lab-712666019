# Digital Image/Video Processing (DVP) Labs

This repository contains practical work for Digital Image/Video Processing. The former `DVP/` wrapper folder has been removed, so every lab folder and dataset folder now lives directly at the repository root.

## Repository Structure

- `Dataset/` — input datasets used by the lab programs.
- `Lab 1/` — basic image processing operations.
- `Lab 2/` — image enhancement using intensity transformation functions.
- `Lab 3/` — histogram equalization, CLAHE, histogram matching, and parameter sweep experiments.
- `Lab 4/` — spatial filtering for degraded autonomous ground vehicle (AGV) camera frames.

## Overall Problem Statement

The objective of this repository is to demonstrate core digital image processing techniques through separate laboratory exercises. Each lab focuses on a specific image-processing topic, implements the required operations in Python, and stores output images or result files that show the effect of each method.

Across the labs, the work covers:

1. Reading, displaying, transforming, and saving images.
2. Enhancing image intensity values using mathematical transformation functions.
3. Improving contrast with histogram-based methods.
4. Restoring and enhancing degraded images using spatial filtering.
5. Comparing outputs visually and, where applicable, quantitatively.

## Lab Summary and Outputs

| Lab | Problem Statement | Main Outputs |
| --- | --- | --- |
| Lab 1 | Perform basic image-processing operations such as grayscale conversion, brightness adjustment, contrast enhancement, resizing, rotation, flipping, cropping, and negative conversion. | Processed images in `Lab 1/Image Output/`, including grayscale, brightness, contrast, resized, rotated, flipped, cropped, and negative results. |
| Lab 2 | Apply negative, gamma/power-law, and logarithmic intensity transformations using both manual pixel-level logic and library/helper-based processing. | Enhanced images in `Lab 2/Lab2_Outputs/`, including manual and library versions of negative, gamma, and log transformations. |
| Lab 3 | Improve image contrast using global histogram equalization, CLAHE, histogram matching, analytical target histograms, and CLAHE parameter sweeps. | Comparison plots and enhanced images in the Lab 3 output folders, including matched images, CDF/histogram comparisons, CLAHE comparisons, and best-parameter results. |
| Lab 4 | Restore and enhance degraded AGV camera imagery using averaging filters, Laplacian sharpening, unsharp masking, high-boost filtering, and quantitative quality metrics. | Degraded images, filtered outputs, comparison grids, metrics CSV/XLSX files, and final pipeline output in `Lab 4/AGV_Spatial_Filtering_Output/`. |

## Requirements

The Python programs use common image-processing and plotting packages:

- Python 3
- OpenCV (`cv2`)
- NumPy
- Matplotlib
- Pandas, for Lab 4 result tables

## How to Use

Open the README file inside each lab folder for the detailed problem statement, input path, implementation notes, output list, and result summary.

Example commands from the repository root:

```bash
python3 "Lab 1/Code/lab1_image_processing.py"
python3 "Lab 2/Code/lab2_image_enhancement.py"
python3 "Lab 4/Code/SPATIAL FILTERING.py"
```

Lab 3 contains multiple scripts, so run the script matching the experiment you want to reproduce from `Lab 3/Code/`.
