# Digital Image Processing Lab — Histogram Matching and CLAHE

## Overview

This README contains the complete solution for two image-enhancement problems:

1. **Histogram Matching (Histogram Specification)**
2. **Adaptive Histogram Equalization with Contrast Limiting (CLAHE)**

The implementations are designed for a Digital Image Processing laboratory. The histogram-matching algorithm and the main CLAHE algorithm are implemented from first principles, while OpenCV is used for image I/O, visualization, and the fast CLAHE parameter sweep.

---

# Problem 1 — Histogram Matching

## 1. Problem Statement

A film restoration studio is digitizing an old movie shot over several days. Because of changing daylight, aging film stock, and different camera rolls, consecutive scenes that are supposed to look identical have different tones.

One frame may be warm and bright while another may be dull and grey, even though they depict the same set.

The studio has selected one hand-graded reference frame and wants every other frame to have the same tonal look.

The appropriate solution is **histogram matching**, also called **histogram specification**.

---

## 2. Objective

Given:

- a source image/frame,
- a reference image/frame,

transform the source image so that its intensity distribution resembles the intensity distribution of the reference image.

Unlike histogram equalization, histogram matching does **not** force the output histogram to become uniform. It forces the output distribution toward a specified target distribution.

---

# 3. Why Histogram Equalization Is Not Suitable

Histogram equalization is designed mainly to improve overall contrast by transforming the image toward an approximately uniform intensity distribution.

That is not what the film-restoration problem requires.

The colorist has already selected a particular tonal appearance. The requirement is:

> Every frame should have the same tonal distribution as the selected reference frame.

Histogram equalization instead produces:

> A generic approximately uniform distribution.

Therefore, histogram equalization violates the application's most important requirement:

**The output must match a specific desired tonal distribution rather than simply maximizing global contrast.**

For example, suppose the reference frame has a deliberately dark, cinematic distribution. Histogram equalization would try to spread the intensities across the complete range, potentially destroying the intended cinematic appearance.

Histogram matching preserves the reference's desired global tonal character.

---

# 4. Mathematical Principle of Histogram Matching

Let:

- `r` = source image intensity
- `s` = transformed intensity
- `p_r(r)` = probability distribution of source intensities
- `p_z(z)` = desired/reference probability distribution

First calculate the source CDF:

\[
T(r)=\sum_{k=0}^{r}p_r(k)
\]

The source intensity is transformed into its cumulative probability:

\[
s=T(r)
\]

Next calculate the reference CDF:

\[
G(z)=\sum_{k=0}^{z}p_z(k)
\]

To obtain the reference intensity corresponding to the source CDF:

\[
z=G^{-1}(T(r))
\]

For a discrete 8-bit image, an exact inverse may not exist. Therefore, for every source intensity, the implementation searches for the reference intensity whose CDF is closest.

The resulting mapping is:

\[
M(r)=\arg\min_z |G(z)-T(r)|
\]

Finally:

\[
output(x,y)=M(source(x,y))
\]

---

# 5. First-Principles Histogram Matching Implementation

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


# =========================================================
# PATHS
# =========================================================

source1_path = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"
source2_path = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"

output_folder = r"C:\Users\yoges\Downloads\Histogram_Matching_Outputs"

os.makedirs(output_folder, exist_ok=True)


# =========================================================
# LOAD IMAGE
# =========================================================

reference = cv2.imread(
    source1_path,
    cv2.IMREAD_GRAYSCALE
)

source1 = cv2.imread(
    source1_path,
    cv2.IMREAD_GRAYSCALE
)

source2 = cv2.imread(
    source2_path,
    cv2.IMREAD_GRAYSCALE
)

if reference is None or source1 is None or source2 is None:
    print("Error loading image!")
    exit()


# =========================================================
# CREATE TWO DIFFERENT EXPOSURES
# =========================================================

# Dark frame
source1 = cv2.convertScaleAbs(
    source1,
    alpha=0.65,
    beta=-30
)

# Bright frame
source2 = cv2.convertScaleAbs(
    source2,
    alpha=1.25,
    beta=40
)


# =========================================================
# HISTOGRAM MATCHING FROM FIRST PRINCIPLES
# =========================================================

def histogram_matching(source, reference):

    # Source histogram
    source_hist = np.bincount(
        source.ravel(),
        minlength=256
    )

    # Reference histogram
    reference_hist = np.bincount(
        reference.ravel(),
        minlength=256
    )

    # Convert histogram to probability distribution
    source_pdf = source_hist / source.size
    reference_pdf = reference_hist / reference.size

    # Calculate CDFs
    source_cdf = np.cumsum(source_pdf)
    reference_cdf = np.cumsum(reference_pdf)

    # Intensity mapping
    mapping = np.zeros(
        256,
        dtype=np.uint8
    )

    for source_intensity in range(256):

        source_value = source_cdf[
            source_intensity
        ]

        difference = np.abs(
            reference_cdf - source_value
        )

        reference_intensity = np.argmin(
            difference
        )

        mapping[source_intensity] = (
            reference_intensity
        )

    # Apply mapping
    output = mapping[source]

    return (
        output,
        source_cdf,
        reference_cdf,
        mapping
    )


# =========================================================
# MATCH BOTH SOURCE FRAMES
# =========================================================

matched1, cdf1, ref_cdf, map1 = (
    histogram_matching(
        source1,
        reference
    )
)

matched2, cdf2, ref_cdf, map2 = (
    histogram_matching(
        source2,
        reference
    )
)


# =========================================================
# SAVE IMAGES
# =========================================================

cv2.imwrite(
    os.path.join(
        output_folder,
        "reference.jpg"
    ),
    reference
)

cv2.imwrite(
    os.path.join(
        output_folder,
        "dark_source.jpg"
    ),
    source1
)

cv2.imwrite(
    os.path.join(
        output_folder,
        "bright_source.jpg"
    ),
    source2
)

cv2.imwrite(
    os.path.join(
        output_folder,
        "matched_dark.jpg"
    ),
    matched1
)

cv2.imwrite(
    os.path.join(
        output_folder,
        "matched_bright.jpg"
    ),
    matched2
)


# =========================================================
# HISTOGRAM FUNCTION
# =========================================================

def get_histogram(image):

    return np.bincount(
        image.ravel(),
        minlength=256
    )


# =========================================================
# IMAGE COMPARISON
# =========================================================

plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.imshow(
    reference,
    cmap="gray"
)
plt.title("Reference")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(
    source1,
    cmap="gray"
)
plt.title("Dark Source")
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(
    matched1,
    cmap="gray"
)
plt.title("Matched Dark")
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(
    source2,
    cmap="gray"
)
plt.title("Bright Source")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(
    matched2,
    cmap="gray"
)
plt.title("Matched Bright")
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(
    reference,
    cmap="gray"
)
plt.title("Target Reference")
plt.axis("off")

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "histogram_matching_images.png"
    ),
    dpi=300
)

plt.show()


# =========================================================
# HISTOGRAM COMPARISON
# =========================================================

plt.figure(figsize=(12, 7))

plt.plot(
    get_histogram(reference),
    label="Reference"
)

plt.plot(
    get_histogram(source1),
    label="Dark Source"
)

plt.plot(
    get_histogram(matched1),
    label="Matched Dark"
)

plt.plot(
    get_histogram(source2),
    label="Bright Source"
)

plt.plot(
    get_histogram(matched2),
    label="Matched Bright"
)

plt.xlabel("Intensity")
plt.ylabel("Frequency")
plt.title("Histogram Matching")

plt.legend()

plt.savefig(
    os.path.join(
        output_folder,
        "histogram_comparison.png"
    ),
    dpi=300
)

plt.show()


# =========================================================
# CDF FUNCTION
# =========================================================

def calculate_cdf(image):

    hist = get_histogram(image)

    pdf = hist / image.size

    return np.cumsum(pdf)


# =========================================================
# CDF COMPARISON
# =========================================================

plt.figure(figsize=(12, 7))

plt.plot(
    calculate_cdf(reference),
    label="Reference CDF"
)

plt.plot(
    calculate_cdf(source1),
    label="Dark Source CDF"
)

plt.plot(
    calculate_cdf(matched1),
    label="Matched Dark CDF"
)

plt.plot(
    calculate_cdf(source2),
    label="Bright Source CDF"
)

plt.plot(
    calculate_cdf(matched2),
    label="Matched Bright CDF"
)

plt.xlabel("Intensity")
plt.ylabel("CDF")
plt.title("CDF Comparison")

plt.legend()

plt.savefig(
    os.path.join(
        output_folder,
        "cdf_comparison.png"
    ),
    dpi=300
)

plt.show()
```

---

# 6. Expected Histogram Matching Result

Before matching:

- The dark source has its histogram shifted toward low intensities.
- The bright source has its histogram shifted toward high intensities.
- The reference has the desired tonal distribution.

After matching:

- The dark source's histogram moves toward the reference.
- The bright source's histogram moves toward the reference.
- Their CDFs become substantially closer to the reference CDF.

The exact histogram will not necessarily be identical because the images are discrete and have different spatial content.

---

# 7. Analytical Target Histogram

A reference image is not mandatory.

A colorist can mathematically define a target distribution.

For a moody, shadow-heavy appearance, a Gaussian-like distribution centered at a low intensity can be used.

```python
def create_moody_target():

    intensity = np.arange(256)

    center = 70
    sigma = 35

    target = np.exp(
        -((intensity - center) ** 2)
        / (2 * sigma ** 2)
    )

    target = target / np.sum(target)

    return target


def histogram_matching_target(
    source,
    target_pdf
):

    source_hist = np.bincount(
        source.ravel(),
        minlength=256
    )

    source_pdf = (
        source_hist /
        source.size
    )

    source_cdf = np.cumsum(
        source_pdf
    )

    target_cdf = np.cumsum(
        target_pdf
    )

    mapping = np.zeros(
        256,
        dtype=np.uint8
    )

    for r in range(256):

        difference = np.abs(
            target_cdf -
            source_cdf[r]
        )

        mapping[r] = np.argmin(
            difference
        )

    return mapping[source]


target_pdf = create_moody_target()

moody_image = histogram_matching_target(
    source1,
    target_pdf
)

cv2.imwrite(
    os.path.join(
        output_folder,
        "moody_target_result.jpg"
    ),
    moody_image
)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)

plt.imshow(
    moody_image,
    cmap="gray"
)

plt.title("Moody Target Result")
plt.axis("off")

plt.subplot(1, 2, 2)

plt.plot(target_pdf)

plt.title(
    "Analytical Target Histogram"
)

plt.xlabel("Intensity")
plt.ylabel("Probability")

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "analytical_target.png"
    ),
    dpi=300
)

plt.show()
```

The target histogram is intentionally concentrated around a lower intensity. Consequently, the resulting image has a darker, shadow-heavy tonal character.

---

# 8. Failure of Histogram Matching

Histogram matching is a **global intensity transformation**.

It does not understand:

- objects,
- edges,
- spatial locations,
- textures,
- scene semantics.

Consider:

**Source:** an outdoor scene containing a bright sky and dark foreground.

**Reference:** a dark indoor scene containing mostly shadows.

Forcing the outdoor image to adopt the indoor image's intensity distribution can cause:

- sky detail to become unnatural,
- highlights to become compressed,
- shadows to become excessive,
- local contrast to be lost,
- noise to become more visible,
- banding or posterization in extreme cases.

The fundamental reason is:

> **A histogram contains intensity information but no spatial information.**

Two completely different images can have similar histograms, and two visually similar images can have different histograms.

Therefore histogram matching is most appropriate when the images have reasonably compatible scene content and the main difference is exposure or tonal appearance.

---

# Problem 2 — CLAHE

# 9. Problem Statement

A medical imaging system processes chest X-rays.

Important lung structures may occupy a relatively narrow range of low intensities, while the same image contains:

- bright bones,
- dark background,
- soft tissue,
- other structures.

Global histogram equalization uses one histogram for the entire image. Large bright and dark regions can therefore dominate the transformation.

The requirement is to improve contrast **locally**:

- reveal faint details in dark regions,
- reveal details in bright regions,
- avoid letting one region control the entire transformation,
- prevent excessive noise amplification.

The appropriate method is:

**CLAHE — Contrast Limited Adaptive Histogram Equalization.**

---

# 10. Why One Global Histogram Is the Wrong Model

Imagine an image containing:

```text
+--------------------------------+
|                                |
|          DARK REGION           |
|                                |
|          lung details          |
|                                |
|     BRIGHT BONE REGION         |
|                                |
+--------------------------------+
```

A global histogram combines pixels from both regions.

Suppose:

- the bright bone occupies a large portion of the image,
- the background occupies another large portion,
- lung texture occupies only a small intensity range.

The global histogram therefore reflects the dominant regions much more strongly than the small lung-detail region.

One mapping is then applied everywhere:

\[
output=T(global\ intensity)
\]

The lung region cannot have its own appropriate transformation.

CLAHE instead divides the image into local tiles:

\[
Image
\rightarrow
Tiles
\rightarrow
Local\ Histograms
\rightarrow
Local\ Equalization
\]

A dark tile can therefore receive a transformation suited to dark pixels while a bright tile receives a different transformation.

This is the fundamental advantage of adaptive histogram equalization.

---

# 11. CLAHE Algorithm

CLAHE consists of four main stages.

## Step 1 — Divide the image into tiles

For example:

```text
+-------+-------+-------+-------+
| Tile  | Tile  | Tile  | Tile  |
+-------+-------+-------+-------+
| Tile  | Tile  | Tile  | Tile  |
+-------+-------+-------+-------+
| Tile  | Tile  | Tile  | Tile  |
+-------+-------+-------+-------+
```

Each tile has its own histogram.

## Step 2 — Clip the histogram

If a histogram bin becomes too large:

\[
h(i)>C
\]

it is clipped:

\[
h(i)=C
\]

The removed excess is redistributed across the histogram.

## Step 3 — Calculate the local CDF

\[
CDF(k)=\sum_{i=0}^{k}h(i)
\]

The CDF is then used to construct the local equalization mapping.

## Step 4 — Bilinear interpolation

Each pixel can be influenced by up to four neighboring tile mappings.

This produces a smooth transition between tiles and prevents visible block boundaries.

---

# 12. Why Contrast Limiting Is Required

Consider a homogeneous tile:

```text
100 100 100 100
100 100 101 100
100 100 100 100
```

There is almost no real detail.

Without contrast limiting, adaptive equalization may interpret the tiny difference between 100 and 101 as important information and strongly amplify it.

The result can be:

- visible noise,
- artificial texture,
- grain,
- distracting artifacts.

CLAHE limits histogram peaks:

\[
h(i)\leq C
\]

and redistributes the excess.

Thus the local histogram cannot produce unlimited contrast amplification.

---

# 13. Why Bilinear Interpolation Is Required

Suppose neighboring tiles have different transformations.

Without interpolation:

```text
Tile A | Tile B
       |
       |  <-- visible boundary
```

A pixel just on one side of the boundary can receive a very different output intensity from a pixel just on the other side.

This creates blocky seams.

CLAHE uses bilinear interpolation between four neighboring tile mappings:

\[
f(x,y)=
(1-a)(1-b)f_{00}
+a(1-b)f_{01}
+(1-a)bf_{10}
+abf_{11}
\]

The transformation therefore changes smoothly across the image.

---

# 14. First-Principles CLAHE Implementation

```python
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


# =========================================================
# IMAGE PATH
# =========================================================

image_path = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"

output_folder = r"C:\Users\yoges\Downloads\CLAHE_Outputs"

os.makedirs(
    output_folder,
    exist_ok=True
)


# =========================================================
# LOAD IMAGE
# =========================================================

img = cv2.imread(
    image_path,
    cv2.IMREAD_GRAYSCALE
)

if img is None:
    print("Error: Image not found!")
    exit()

print("Image loaded successfully!")
print("Image size:", img.shape)


# =========================================================
# GLOBAL HISTOGRAM EQUALIZATION
# =========================================================

global_equalized = cv2.equalizeHist(
    img
)

cv2.imwrite(
    os.path.join(
        output_folder,
        "global_equalization.jpg"
    ),
    global_equalized
)


# =========================================================
# ENTROPY FUNCTION
# =========================================================

def entropy(image):

    hist = np.bincount(
        image.ravel(),
        minlength=256
    )

    probability = (
        hist /
        image.size
    )

    probability = probability[
        probability > 0
    ]

    return -np.sum(
        probability *
        np.log2(probability)
    )


# =========================================================
# CLAHE FROM SCRATCH
# =========================================================

def clahe_from_scratch(
    image,
    tile_rows=8,
    tile_cols=8,
    clip_limit=2.0
):

    image = image.astype(
        np.uint8
    )

    height, width = image.shape

    tile_height = (
        height /
        tile_rows
    )

    tile_width = (
        width /
        tile_cols
    )

    mappings = []

    # =====================================================
    # LOCAL HISTOGRAMS
    # =====================================================

    for tr in range(tile_rows):

        row_mappings = []

        for tc in range(tile_cols):

            y1 = int(
                tr *
                tile_height
            )

            y2 = int(
                (tr + 1) *
                tile_height
            )

            x1 = int(
                tc *
                tile_width
            )

            x2 = int(
                (tc + 1) *
                tile_width
            )

            tile = image[
                y1:y2,
                x1:x2
            ]

            hist = np.bincount(
                tile.ravel(),
                minlength=256
            ).astype(
                np.float64
            )

            # =================================================
            # CLIP HISTOGRAM
            # =================================================

            tile_area = tile.size

            clip_value = max(
                1,
                int(
                    clip_limit *
                    tile_area /
                    256
                )
            )

            excess = 0

            for i in range(256):

                if hist[i] > clip_value:

                    excess += (
                        hist[i] -
                        clip_value
                    )

                    hist[i] = (
                        clip_value
                    )

            # Redistribute excess
            hist += (
                excess /
                256
            )

            # =================================================
            # CDF
            # =================================================

            cdf = np.cumsum(
                hist
            )

            cdf_min = cdf[0]
            cdf_max = cdf[-1]

            if cdf_max != cdf_min:

                mapping = (
                    (cdf - cdf_min)
                    /
                    (cdf_max - cdf_min)
                    * 255
                )

            else:

                mapping = np.arange(
                    256
                )

            mapping = np.clip(
                mapping,
                0,
                255
            )

            row_mappings.append(
                mapping
            )

        mappings.append(
            row_mappings
        )

    # =====================================================
    # BILINEAR INTERPOLATION
    # =====================================================

    output = np.zeros_like(
        image
    )

    for y in range(height):

        for x in range(width):

            gy = (
                y /
                tile_height
                - 0.5
            )

            gx = (
                x /
                tile_width
                - 0.5
            )

            y0 = int(
                np.floor(gy)
            )

            x0 = int(
                np.floor(gx)
            )

            y1 = y0 + 1
            x1 = x0 + 1

            y0 = max(
                0,
                min(
                    tile_rows - 1,
                    y0
                )
            )

            y1 = max(
                0,
                min(
                    tile_rows - 1,
                    y1
                )
            )

            x0 = max(
                0,
                min(
                    tile_cols - 1,
                    x0
                )
            )

            x1 = max(
                0,
                min(
                    tile_cols - 1,
                    x1
                )
            )

            dy = (
                gy -
                np.floor(gy)
            )

            dx = (
                gx -
                np.floor(gx)
            )

            dy = np.clip(
                dy,
                0,
                1
            )

            dx = np.clip(
                dx,
                0,
                1
            )

            intensity = int(
                image[y, x]
            )

            f00 = mappings[y0][x0][
                intensity
            ]

            f01 = mappings[y0][x1][
                intensity
            ]

            f10 = mappings[y1][x0][
                intensity
            ]

            f11 = mappings[y1][x1][
                intensity
            ]

            value = (
                (1 - dx) *
                (1 - dy) *
                f00
                +
                dx *
                (1 - dy) *
                f01
                +
                (1 - dx) *
                dy *
                f10
                +
                dx *
                dy *
                f11
            )

            output[y, x] = np.clip(
                value,
                0,
                255
            )

    return output.astype(
        np.uint8
    )


# =========================================================
# APPLY CLAHE
# =========================================================

print(
    "\nRunning CLAHE from scratch..."
)

clahe_result = clahe_from_scratch(
    img,
    tile_rows=8,
    tile_cols=8,
    clip_limit=2.0
)

print(
    "CLAHE completed!"
)


# =========================================================
# SAVE CLAHE
# =========================================================

cv2.imwrite(
    os.path.join(
        output_folder,
        "clahe_from_scratch.jpg"
    ),
    clahe_result
)


# =========================================================
# DISPLAY COMPARISON
# =========================================================

plt.figure(
    figsize=(15, 5)
)

plt.subplot(1, 3, 1)

plt.imshow(
    img,
    cmap="gray"
)

plt.title(
    "Original"
)

plt.axis("off")


plt.subplot(1, 3, 2)

plt.imshow(
    global_equalized,
    cmap="gray"
)

plt.title(
    "Global Equalization"
)

plt.axis("off")


plt.subplot(1, 3, 3)

plt.imshow(
    clahe_result,
    cmap="gray"
)

plt.title(
    "CLAHE"
)

plt.axis("off")


plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "CLAHE_Comparison.png"
    ),
    dpi=200
)

plt.show()


# =========================================================
# ENTROPY COMPARISON
# =========================================================

print(
    "\n=============================================="
)

print(
    "             ENTROPY COMPARISON"
)

print(
    "=============================================="
)

print(
    "Original Image Entropy :",
    round(
        entropy(img),
        4
    )
)

print(
    "Global Equalization    :",
    round(
        entropy(
            global_equalized
        ),
        4
    )
)

print(
    "CLAHE                  :",
    round(
        entropy(
            clahe_result
        ),
        4
    )
)
```

---

# 15. Fast CLAHE Parameter Sweep

The first-principles CLAHE implementation contains Python loops over individual pixels. Running it repeatedly for many parameter combinations can therefore be slow.

For the parameter sweep, an optimized OpenCV implementation is used. The algorithmic demonstration remains from first principles; the optimized implementation is used only to efficiently study parameter effects.

The sweep uses:

- Clip limits: `0.5, 1, 2, 4, 8`
- Tile sizes: `2×2, 4×4, 8×8, 16×16`

```python
# =========================================================
# FAST PARAMETER SWEEP
# =========================================================

clip_values = [
    0.5,
    1.0,
    2.0,
    4.0,
    8.0
]

tile_values = [
    2,
    4,
    8,
    16
]

results = []


for tile in tile_values:

    for clip in clip_values:

        # Optimized OpenCV CLAHE
        clahe = cv2.createCLAHE(
            clipLimit=clip,
            tileGridSize=(
                tile,
                tile
            )
        )

        result = clahe.apply(
            img
        )

        # Quantitative metric
        ent = entropy(
            result
        )

        results.append(
            (
                tile,
                clip,
                ent
            )
        )


# =========================================================
# PRINT RESULTS
# =========================================================

print(
    "\n=============================================="
)

print(
    "        CLAHE PARAMETER SWEEP RESULTS"
)

print(
    "=============================================="
)

print(
    f"{'Tile Size':<15}"
    f"{'Clip Limit':<15}"
    f"{'Entropy':<15}"
)

print(
    "-" * 45
)


for tile, clip, ent in results:

    print(
        f"{tile:<15}"
        f"{clip:<15}"
        f"{ent:<15.4f}"
    )


# =========================================================
# FIND HIGHEST ENTROPY
# =========================================================

best_result = max(
    results,
    key=lambda x: x[2]
)

best_tile = best_result[0]
best_clip = best_result[1]
best_entropy = best_result[2]


print(
    "\n=============================================="
)

print(
    "             BEST RESULT"
)

print(
    "=============================================="
)

print(
    "Best Tile Size :",
    best_tile
)

print(
    "Best Clip Limit:",
    best_clip
)

print(
    "Highest Entropy:",
    round(
        best_entropy,
        4
    )
)


# =========================================================
# CREATE BEST IMAGE
# =========================================================

best_clahe = cv2.createCLAHE(
    clipLimit=best_clip,
    tileGridSize=(
        best_tile,
        best_tile
    )
)

best_image = best_clahe.apply(
    img
)


# =========================================================
# SAVE BEST IMAGE
# =========================================================

cv2.imwrite(
    os.path.join(
        output_folder,
        "best_CLAHE_result.jpg"
    ),
    best_image
)


# =========================================================
# ENTROPY PLOT
# =========================================================

plt.figure(
    figsize=(10, 6)
)

for tile in tile_values:

    entropy_values = []

    for t, clip, ent in results:

        if t == tile:

            entropy_values.append(
                ent
            )

    plt.plot(
        clip_values,
        entropy_values,
        marker="o",
        label=f"Tile {tile}x{tile}"
    )


plt.xlabel(
    "Clip Limit"
)

plt.ylabel(
    "Entropy"
)

plt.title(
    "CLAHE Parameter Sweep - Entropy"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "CLAHE_Parameter_Sweep.png"
    ),
    dpi=200
)

plt.show()


# =========================================================
# BEST RESULT COMPARISON
# =========================================================

plt.figure(
    figsize=(10, 5)
)

plt.subplot(1, 2, 1)

plt.imshow(
    img,
    cmap="gray"
)

plt.title(
    "Original"
)

plt.axis("off")


plt.subplot(1, 2, 2)

plt.imshow(
    best_image,
    cmap="gray"
)

plt.title(
    f"Best CLAHE\n"
    f"Tile={best_tile}, "
    f"Clip={best_clip}"
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "Best_CLAHE_Comparison.png"
    ),
    dpi=200
)

plt.show()


print(
    "\nExperiment completed!"
)

print(
    "Outputs saved to:"
)

print(
    output_folder
)
```

---

# 16. CLAHE Parameter Analysis

## Clip Limit

The clip limit controls how strongly local histogram peaks are allowed to dominate.

### Very low clip limit

```text
Clip limit ↓
     ↓
Strong clipping
     ↓
Less contrast enhancement
     ↓
Some details remain hidden
```

### Moderate clip limit

```text
Moderate clipping
       ↓
Local contrast enhancement
       ↓
Details become visible
       ↓
Noise remains reasonably controlled
```

### Very high clip limit

```text
Clip limit ↑
     ↓
Less histogram restriction
     ↓
Strong local contrast
     ↓
Noise amplification
     ↓
Artificial texture
```

Therefore, an excessively high clip limit can produce an unnatural image.

---

# 17. Tile Size Analysis

## Large Tiles

For example:

```text
2 × 2
```

The image is divided into only a few large regions.

The method becomes less adaptive and approaches global histogram equalization.

### Failure mode

- reduced local adaptation,
- small details may remain hidden,
- local intensity variations are not handled independently.

---

## Small Tiles

For example:

```text
16 × 16
```

The image is divided into many small regions.

### Advantages

- stronger local adaptation,
- small details become more visible.

### Failure modes

- noise amplification,
- excessive local contrast,
- artificial texture,
- potentially unnatural appearance.

---

# 18. Quantitative Evaluation Using Entropy

Image entropy is calculated as:

\[
H=-\sum_i p(i)\log_2 p(i)
\]

where:

- \(p(i)\) is the probability of intensity \(i\),
- \(H\) is the image entropy.

Higher entropy generally indicates a broader and more varied intensity distribution.

However:

> **Higher entropy does not automatically mean better image quality.**

Noise can also increase entropy.

Therefore, entropy should be combined with visual inspection or another local-contrast/noise metric when judging medical-image enhancement.

---

# 19. Expected Results

The experiment should demonstrate:

### Global Equalization

- Uses one histogram.
- Bright and dark regions influence the same transformation.
- Some local details may remain poorly enhanced.

### CLAHE

- Uses separate local histograms.
- Dark and bright regions receive different local transformations.
- Fine local details become more visible.
- Contrast limiting reduces excessive amplification.
- Bilinear interpolation reduces tile-boundary artifacts.

---

# 20. Histogram Matching vs CLAHE

| Feature | Histogram Matching | CLAHE |
|---|---|---|
| Main purpose | Match a desired tonal distribution | Improve local contrast |
| Histogram | Reference/global target | Local tile histograms |
| Spatial adaptation | No | Yes |
| Target distribution | Specific reference or analytical distribution | Local equalization |
| Good for exposure normalization | Yes | Sometimes |
| Good for local details | Limited | Yes |
| Noise control | Limited | Contrast limiting |
| Boundary handling | Not applicable | Bilinear interpolation |
| Main failure | Spatial/semantic mismatch | Noise or excessive local enhancement |

---

# 21. Final Conclusion

## Histogram Matching

Histogram matching is appropriate when the goal is to make the tonal appearance of a source image follow a specific reference. The method calculates the source and reference CDFs and constructs an intensity mapping:

\[
z=G^{-1}(T(r))
\]

The two differently exposed source frames can therefore be transformed toward the same reference distribution. An analytical target histogram can also be used when a desired style does not exist in an actual reference frame.

Histogram equalization is unsuitable for this application because it attempts to create an approximately uniform distribution rather than reproducing the colorist's chosen tonal distribution.

Histogram matching can fail when source and reference images have substantially different spatial content because the histogram contains no spatial or semantic information.

## CLAHE

CLAHE is appropriate when important information occurs in different local intensity ranges. It divides the image into tiles, calculates local histograms, clips excessive histogram peaks, redistributes the excess, computes local mappings, and uses bilinear interpolation between neighboring tiles.

Contrast limiting reduces noise amplification in homogeneous regions, while bilinear interpolation prevents visible seams between tiles.

The parameter sweep demonstrates that clip limit and tile size strongly influence the result. Excessively high clip limits can amplify noise, while excessively low values can under-enhance the image. Large tiles reduce local adaptivity, while very small tiles can over-enhance local noise and texture.

Therefore:

> **Histogram matching is best when a specific global tonal look must be reproduced, whereas CLAHE is best when local contrast enhancement is required across regions with different brightness characteristics.**

---

# 22. Output Files

The programs save their results in:

```text
C:\Users\yoges\Downloads\Histogram_Matching_Outputs
```

and:

```text
C:\Users\yoges\Downloads\CLAHE_Outputs
```

Typical outputs include:

```text
Histogram_Matching_Outputs/
│
├── reference.jpg
├── dark_source.jpg
├── bright_source.jpg
├── matched_dark.jpg
├── matched_bright.jpg
├── histogram_matching_images.png
├── histogram_comparison.png
├── cdf_comparison.png
├── moody_target_result.jpg
└── analytical_target.png
```

```text
CLAHE_Outputs/
│
├── global_equalization.jpg
├── clahe_from_scratch.jpg
├── CLAHE_Comparison.png
├── best_CLAHE_result.jpg
├── CLAHE_Parameter_Sweep.png
└── Best_CLAHE_Comparison.png
```

---

# 23. Viva Questions and Short Answers

### Q1. What is histogram matching?

Histogram matching is a transformation technique that modifies an image so that its intensity distribution resembles a specified reference distribution.

### Q2. How is it different from histogram equalization?

Equalization generally targets a uniform distribution, while histogram matching targets a specified distribution.

### Q3. What is a CDF?

CDF is the cumulative distribution function. It represents the cumulative probability up to a particular intensity.

### Q4. What is CLAHE?

CLAHE stands for Contrast Limited Adaptive Histogram Equalization.

### Q5. Why is CLAHE called adaptive?

Because each local tile has its own histogram and transformation.

### Q6. Why is contrast limiting required?

It prevents very frequent intensity values from producing excessive local contrast and helps reduce noise amplification.

### Q7. Why is interpolation used?

Interpolation creates smooth transitions between neighboring tile mappings and prevents blocky seams.

### Q8. What happens when the tile size is too large?

The method becomes less local and approaches global histogram equalization.

### Q9. What happens when the tile size is too small?

Local contrast becomes very strong and noise can be amplified.

### Q10. Does maximum entropy always mean the best image?

No. Noise can also increase entropy, so entropy should not be used alone to judge image quality.
