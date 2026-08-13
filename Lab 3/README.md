# Lab 3 — Histogram Equalization, CLAHE, and Histogram Matching

## Problem Statement

Apply histogram-based enhancement techniques to improve image contrast and compare the visual effect of different contrast-enhancement methods. The lab focuses on global histogram equalization, Contrast Limited Adaptive Histogram Equalization (CLAHE), histogram matching, analytical target histograms, and CLAHE parameter tuning.

## Experiments Implemented

1. Global histogram equalization to redistribute intensity values across the available range.
2. First-principles CLAHE implementation to improve local contrast while limiting over-amplification.
3. Histogram matching to transform source images so their intensity distribution follows a reference image.
4. Analytical target histogram generation and matching.
5. CLAHE parameter sweep to compare different clip limits and tile sizes.

## Input

The Lab 3 dataset folder is:

```text
Dataset/Lab 3/
```

The scripts in `Lab 3/Code/` generate or process the images needed for the individual experiments.

## Output

Lab 3 produces enhanced images and comparison plots in these folders:

- `Lab 3/CLAHE_Outputs/`
  - `global_equalization.jpg`
- `Lab 3/Run CLAHE output/`
  - `CLAHE_comparison.png`
  - `clahe_from_scratch.jpg`
- `Lab 3/Histogram_Matching_Outputs/`
  - `bright_source.jpg`
  - `dark_source.jpg`
  - `reference.jpg`
  - `matched_bright.jpg`
  - `matched_dark.jpg`
  - `histogram_matching_images.png`
  - `histogram_comparison.png`
  - `cdf_comparison.png`
- `Lab 3/Analytical Target Histogram outputs/`
  - `analytical_target.png`
  - `moody_target_result.jpg`
- `Lab 3/Parameter Sweep output/`
  - `CLAHE_Parameter_Sweep.png`
  - `CLAHE_Comparison.png`
  - `Best_CLAHE_Comparison.png`
  - `best_CLAHE_result.jpg`
  - `clahe_from_scratch.jpg`
  - `global_equalization.jpg`

## How to Run

Run the required experiment script from the repository root:

```bash
python3 "Lab 3/Code/Run CLAHE.py"
python3 "Lab 3/Code/First-Principles CLAHE Implementation.py"
python3 "Lab 3/Code/First-Principles Histogram Matching.py"
python3 "Lab 3/Code/Analytical Target Histogram.py"
python3 "Lab 3/Code/Parameter Sweep.py"
```

## Result

The outputs show that global histogram equalization improves overall contrast but may over-enhance some regions. CLAHE gives better local contrast control by processing small tiles and limiting contrast amplification. Histogram matching changes a source image so its histogram and cumulative distribution become closer to a selected reference or analytical target. The parameter sweep helps choose CLAHE settings that balance contrast improvement with natural image appearance.
