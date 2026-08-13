# Lab 2 — Image Enhancement Using Transformation Functions

## Problem Statement

Implement basic image enhancement techniques using intensity transformation functions. Each transformation is performed in two ways: manually with pixel-level logic and with library/helper operations. The goal is to understand how mathematical transformations change image brightness, contrast, and intensity distribution.

## Transformations Implemented

### Negative Transformation

For an 8-bit image, the negative transformation is:

```text
s = 255 - r
```

This reverses intensity levels, making dark regions bright and bright regions dark.

### Power-Law / Gamma Transformation

The gamma transformation is:

```text
s = c * r^gamma
```

- `gamma < 1` brightens the image.
- `gamma = 1` keeps the image approximately unchanged.
- `gamma > 1` darkens the image.

### Logarithmic Transformation

The log transformation is:

```text
s = c * log(1 + r)
```

This expands low intensity values and compresses high intensity values, which can reveal details in darker regions.

## Input

The script is designed to load a grayscale version of `Cloudhoppers.jpg`.

Dataset/reference file in this repository:

```text
Dataset/Lab 2/sample.ppm
```

## Output

Generated output images are stored in:

```text
Lab 2/Lab2_Outputs/
```

The output folder contains:

- `negative_without_library.jpg`
- `negative_with_library.jpg`
- `gamma_without_library.jpg`
- `gamma_with_library.jpg`
- `log_without_library.jpg`
- `log_with_library.jpg`

## How to Run

From the repository root:

```bash
python3 "Lab 2/Code/lab2_image_enhancement.py"
```

On Windows:

```bash
python "Lab 2/Code/lab2_image_enhancement.py"
```

> Note: The script currently contains local absolute Windows paths for the input image and output folder. Update those paths before running on a different machine.

## Result

The manual and library-based outputs demonstrate the same enhancement concepts. Negative transformation reverses intensity values, gamma correction changes brightness non-linearly, and log transformation improves visibility in darker regions by expanding low intensity values.
