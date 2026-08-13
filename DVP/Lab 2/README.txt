# Lab 2 — Image Enhancement: Transformation Functions

## Aim

To implement and study basic **image enhancement transformation functions** manually and using reusable helper/tool functions, and to observe their effect on image intensity values.

---

## Transformations Studied

### 1. Negative Transformation

The negative transformation is given by:

[
S = L - 1 - r
]

where:

* `r` = input pixel intensity
* `S` = output pixel intensity
* `L` = number of intensity levels

For an 8-bit grayscale image:

[
L = 256
]

Therefore:

[
S = 255-r
]

The transformation reverses the intensity levels. Dark pixels become bright and bright pixels become dark.

---

### 2. Power-Law / Gamma Correction

The power-law transformation is:

[
S = c(r^\gamma)
]

where:

* `r` = normalized input intensity
* `S` = output intensity
* `c` = scaling constant
* `γ` = gamma value

Gamma correction provides **non-linear control over image brightness**.

* `γ < 1` → image becomes brighter
* `γ = 1` → approximately unchanged
* `γ > 1` → image becomes darker

---

### 3. Log Transformation

The log transformation is:

[
S = c\log(1+r)
]

It expands the lower intensity values while compressing higher intensity values.

This makes the transformation particularly useful when important information is concentrated in darker regions of an image.

---

## Implementation

Two implementations were developed:

### Manual Implementation

The transformations were implemented directly using loops over the image pixels.

```text
Image
  ↓
Read pixel
  ↓
Apply mathematical transformation
  ↓
Calculate new intensity
  ↓
Store output pixel
```

This approach demonstrates how the transformation equations operate at the individual-pixel level.

### Tool / Helper Implementation

Reusable helper functions were used to perform the same transformations.

The helper-based implementation reduces repeated code and makes it easier to apply different transformation functions and parameter values.

---

## How to Run

From the project root, run:

```bash
python3 "DVP/Lab 2/Code/lab2_image_enhancement.py"
```

For Windows, the following can also be used:

```bash
python "DVP/Lab 2/Code/lab2_image_enhancement.py"
```

---

## Input Dataset

The experiment uses:

```text
DVP/Dataset/Lab 2/sample.ppm
```

---

## Output

All generated images are stored in:

```text
DVP/Lab 2/Image Output/
```

The program generates results for:

```text
Original Image
Manual Negative
Manual Gamma
Manual Log
Tool Negative
Tool Gamma
Tool Log
```

The manual and helper-based results can be compared to verify that both implementations produce equivalent transformations.

---

## Result

The experiment successfully implemented all three image enhancement transformations using both manual pixel-level processing and reusable helper functions.

### Negative Transformation

The negative transformation reversed the intensity values of the image. Bright regions became dark and dark regions became bright.

### Gamma Correction

Gamma correction changed the image brightness according to the selected gamma value. It demonstrated that image intensity can be adjusted non-linearly rather than simply adding or subtracting a constant brightness value.

### Log Transformation

The log transformation expanded darker intensity values and compressed brighter values. As a result, details present in darker regions became more visible.

The manual and helper-based implementations produced comparable results, demonstrating that the mathematical transformations were correctly implemented.

---

## What I Learned

* The **negative transformation** reverses the intensity levels of an image.
* **Gamma correction** provides non-linear control over image brightness.
* `γ < 1` generally brightens an image, while `γ > 1` generally darkens it.
* **Log transformation** expands low-intensity values and compresses high-intensity values.
* Image enhancement transformations operate by modifying the **intensity of individual pixels**.
* Implementing the formulas manually helps in understanding the underlying image-processing operations.
* Reusable helper functions reduce code duplication and make experimentation easier.
* Different transformations are useful for different image characteristics and enhancement requirements.

---

## Conclusion

The experiment successfully demonstrated three fundamental **intensity transformation techniques** used in digital image processing: **negative, power-law/gamma, and logarithmic transformations**.

Both manual and reusable helper-based implementations were developed and compared. The experiment shows how mathematical transformations can modify image intensity distributions to improve the visibility of specific features and regions in an image.
