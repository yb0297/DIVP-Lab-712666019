# Lab 1 — Basic Image Processing Operations

## Problem Statement

Write a Python program to perform common image-processing operations on an input image and save the processed outputs. The lab demonstrates how a digital image can be inspected, modified, geometrically transformed, and exported for later comparison.

## Operations Implemented

1. Display the original image.
2. Display image properties such as width, height, channels, data type, and total pixels.
3. Convert the image to grayscale.
4. Increase image brightness.
5. Increase image contrast.
6. Resize the image.
7. Rotate the image.
8. Flip the image.
9. Crop the image.
10. Generate the negative image.
11. Save the processed result.

## Input

The program is written to process a hot-air-balloon image named `Cloudhoppers.jpg`.

In this repository, the generated output images are stored in:

```text
Lab 1/Image Output/
```

## Output

The lab produces the following output images:

- `Cloudhoppers.jpg` — original/reference output image.
- `grayscale.jpg` — grayscale version of the image.
- `brightness.jpg` — brightness-enhanced image.
- `contrast.jpg` — contrast-enhanced image.
- `resized.jpg` — resized image.
- `rotated.jpg` — rotated image.
- `flipped.jpg` — flipped image.
- `cropped.jpg` — cropped region of the image.
- `negative.jpg` — intensity-inverted negative image.

## How to Run

From the repository root:

```bash
python3 "Lab 1/Code/lab1_image_processing.py"
```

On Windows:

```bash
python "Lab 1/Code/lab1_image_processing.py"
```

> Note: The script currently contains local absolute Windows paths for the input image and output folder. Update those paths before running on a different machine.

## Result

The experiment successfully demonstrates basic digital image-processing operations. The output images show how pixel intensity operations change brightness, contrast, grayscale values, and negative representation, while geometric operations change image size, orientation, and selected region.
