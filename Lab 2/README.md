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
