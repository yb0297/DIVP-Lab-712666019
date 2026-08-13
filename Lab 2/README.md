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
# Lab 2 — Image Enhancement: Transformation Functions

## Aim

To implement basic image enhancement transformation functions **manually and using reusable helper/tool functions**, and observe their effect on image intensity values.

---

## Transformations

### 1. Negative Transformation

[
S = L - 1 - r
]

For an 8-bit image:

[
S = 255-r
]

The negative transformation reverses the intensity levels of an image.

---

### 2. Power-Law / Gamma Correction

[
S = c(r^\gamma)
]

Gamma correction changes image brightness non-linearly.

* `γ < 1` → brighter image
* `γ = 1` → approximately unchanged
* `γ > 1` → darker image

---

### 3. Log Transformation

[
S = c\log(1+r)
]

The log transformation expands darker intensity values and compresses brighter intensity values. It can therefore make details in dark regions more visible.

---

## Implementation

The experiment contains **two implementations** for each transformation.

### Manual Implementation

The transformation is implemented using direct loops over the pixels.

```text
Input Image
     ↓
Read Pixel
     ↓
Apply Transformation Formula
     ↓
Calculate Output Intensity
     ↓
Store Pixel
     ↓
Output Image
```

This implementation helps understand how image enhancement works at the individual-pixel level.

### Tool / Helper Implementation

Reusable image helper functions and `map_pixels` are used to apply the transformations.

This approach reduces repeated code and makes it easier to experiment with different transformations and parameters.

---

## Input

The input image used for the experiment is:

```text
DVP/Dataset/Lab 2/sample.ppm
```

---

## Output

Generated images are saved in:

```text
DVP/Lab 2/Image Output/
```

The program generates:

```text
Original Image
Manual Negative
Manual Gamma
Manual Log
Tool Negative
Tool Gamma
Tool Log
```

---

## How to Run

From the project root:

```bash
python3 "DVP/Lab 2/Code/lab2_image_enhancement.py"
```

On Windows:

```bash
python "Lab 2/Code/lab2_image_enhancement.py"
```

> Note: The script currently contains local absolute Windows paths for the input image and output folder. Update those paths before running on a different machine.

## Result

The manual and library-based outputs demonstrate the same enhancement concepts. Negative transformation reverses intensity values, gamma correction changes brightness non-linearly, and log transformation improves visibility in darker regions by expanding low intensity values.
python "DVP/Lab 2/Code/lab2_image_enhancement.py"
```

---

## Results

### Negative

The negative transformation reversed the intensity values. Bright regions became dark and dark regions became bright.

### Gamma Correction

Gamma correction modified the brightness of the image non-linearly. Different gamma values produced different levels of brightness modification.

### Log Transformation

The log transformation expanded lower intensity values and compressed higher intensity values, making information in darker regions more visible.

The manual and helper-based implementations produced comparable transformation results.

---

## What I Learned

* Negative transformation reverses image intensity values.
* Gamma correction provides non-linear brightness adjustment.
* `γ < 1` generally brightens an image.
* `γ > 1` generally darkens an image.
* Log transformation expands dark intensity values and compresses bright intensity values.
* Image enhancement transformations can be implemented directly at the pixel level.
* Manual implementation helps understand the mathematical operation behind each transformation.
* Reusable helper functions reduce code duplication and simplify experimentation.

---

## Conclusion

The experiment successfully implemented **Negative, Power-Law/Gamma, and Logarithmic transformations** using both manual pixel-level processing and reusable helper functions.

The results demonstrate how intensity transformation functions can modify an image's intensity values to enhance specific visual characteristics and improve the visibility of important image regions.
