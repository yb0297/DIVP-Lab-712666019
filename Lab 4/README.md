# Lab 4 — Spatial Filtering for Degraded AGV Camera Images

## Problem Statement

Restore and enhance degraded onboard camera images for an Autonomous Ground Vehicle (AGV). The lab simulates degradation such as Gaussian noise and motion blur, then applies spatial filtering methods to reduce noise, sharpen boundaries, and support later tasks such as obstacle detection and terrain classification.

## Tasks Implemented

1. Generate degraded images from a clean reference image.
2. Apply averaging filters with different kernel sizes for noise suppression.
3. Apply 4-neighbor and 8-neighbor Laplacian filters for edge enhancement.
4. Apply unsharp masking and high-boost filtering with different `k` values.
5. Compare pipeline orders for denoising and sharpening.
6. Evaluate processed outputs using PSNR and Laplacian-variance sharpness metrics.

## Input

The script is designed to process `Cloudhoppers.jpg` as the clean reference image.

Dataset/reference folder in this repository:

```text
Dataset/Lab 4/
```

## Output

Generated results are stored in:

```text
Lab 4/AGV_Spatial_Filtering_Output/
```

Important output folders and files include:

- `01_Degraded/` — clean reference, noisy images, and motion-blurred image.
- `02_Task1_Averaging/` — averaging-filter outputs for multiple noise levels and kernel sizes.
- `03_Task2_Laplacian/` — Laplacian response and sharpened images.
- `04_Task3_HighBoost/` — high-boost filtering results for multiple `k` values.
- `05_Grids/` — comparison grids and metric plots.
- `06_Results/` — summary files, CSV/XLSX metrics tables, extra-noise outputs, pipeline comparison, and final pipeline result.

## How to Run

From the repository root:

```bash
python3 "Lab 4/Code/SPATIAL FILTERING.py"
```

On Windows:

```bash
python "Lab 4/Code/SPATIAL FILTERING.py"
```

> Note: The script currently contains local absolute Windows paths for the input image and output folder. Update those paths before running on a different machine.

## Result

The experiment shows the trade-off between smoothing and sharpening. Larger averaging kernels suppress more noise but blur important edges. Laplacian and high-boost filters improve boundary visibility but can also amplify noise if applied too strongly. The recommended approach is a two-stage pipeline: moderate denoising followed by controlled sharpening.
