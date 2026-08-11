import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


# =========================================================
# IMAGE PATH
# =========================================================

image_path = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"

output_folder = r"C:\Users\yoges\Downloads\CLAHE_Outputs"

os.makedirs(output_folder, exist_ok=True)


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

global_equalized = cv2.equalizeHist(img)

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

    probability = hist / image.size

    probability = probability[
        probability > 0
    ]

    return -np.sum(
        probability * np.log2(probability)
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

    image = image.astype(np.uint8)

    height, width = image.shape

    # -----------------------------------------------------
    # TILE SIZE
    # -----------------------------------------------------

    tile_height = height / tile_rows
    tile_width = width / tile_cols

    # Store mappings
    mappings = []

    # =====================================================
    # CREATE LOCAL HISTOGRAMS
    # =====================================================

    for tr in range(tile_rows):

        row_mappings = []

        for tc in range(tile_cols):

            # Tile coordinates
            y1 = int(tr * tile_height)
            y2 = int((tr + 1) * tile_height)

            x1 = int(tc * tile_width)
            x2 = int((tc + 1) * tile_width)

            # Extract tile
            tile = image[
                y1:y2,
                x1:x2
            ]

            # ------------------------------------------------
            # HISTOGRAM
            # ------------------------------------------------

            hist = np.bincount(
                tile.ravel(),
                minlength=256
            ).astype(np.float64)

            # ------------------------------------------------
            # CLIP LIMIT
            # ------------------------------------------------

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

                    hist[i] = clip_value

            # ------------------------------------------------
            # REDISTRIBUTE EXCESS
            # ------------------------------------------------

            hist += excess / 256

            # ------------------------------------------------
            # CDF
            # ------------------------------------------------

            cdf = np.cumsum(hist)

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

                mapping = np.arange(256)

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

    output = np.zeros_like(image)

    for y in range(height):

        for x in range(width):

            # Position inside tile grid
            gy = (
                y / tile_height
                - 0.5
            )

            gx = (
                x / tile_width
                - 0.5
            )

            y0 = int(np.floor(gy))
            x0 = int(np.floor(gx))

            y1 = y0 + 1
            x1 = x0 + 1

            # Keep indices inside image
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

            # ------------------------------------------------
            # FRACTIONAL POSITION
            # ------------------------------------------------

            dy = gy - np.floor(gy)
            dx = gx - np.floor(gx)

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

            # Pixel intensity
            intensity = int(
                image[y, x]
            )

            # ------------------------------------------------
            # FOUR NEIGHBOURING TILE VALUES
            # ------------------------------------------------

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

            # ------------------------------------------------
            # BILINEAR INTERPOLATION
            # ------------------------------------------------

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
# APPLY CLAHE FROM SCRATCH
# =========================================================

print("\nRunning CLAHE from scratch...")

clahe_result = clahe_from_scratch(
    img,
    tile_rows=8,
    tile_cols=8,
    clip_limit=2.0
)

print("CLAHE from scratch completed!")


# =========================================================
# SAVE CLAHE RESULT
# =========================================================

cv2.imwrite(
    os.path.join(
        output_folder,
        "clahe_from_scratch.jpg"
    ),
    clahe_result
)


# =========================================================
# DISPLAY ORIGINAL VS GLOBAL VS CLAHE
# =========================================================

plt.figure(
    figsize=(15, 5)
)


plt.subplot(1, 3, 1)

plt.imshow(
    img,
    cmap="gray"
)

plt.title("Original")

plt.axis("off")


plt.subplot(1, 3, 2)

plt.imshow(
    global_equalized,
    cmap="gray"
)

plt.title(
    "Global Histogram Equalization"
)

plt.axis("off")


plt.subplot(1, 3, 3)

plt.imshow(
    clahe_result,
    cmap="gray"
)

plt.title(
    "CLAHE From Scratch"
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

original_entropy = entropy(img)

global_entropy = entropy(
    global_equalized
)

clahe_entropy = entropy(
    clahe_result
)


print("\n==============================================")
print("             ENTROPY COMPARISON")
print("==============================================")

print(
    "Original Image Entropy :",
    round(original_entropy, 4)
)

print(
    "Global Equalization    :",
    round(global_entropy, 4)
)

print(
    "CLAHE                  :",
    round(clahe_entropy, 4)
)


# =========================================================
# FAST PARAMETER SWEEP
# =========================================================
#
# IMPORTANT:
# We use OpenCV CLAHE here because the parameter sweep
# requires 20 CLAHE operations.
#
# The from-scratch implementation above is retained for
# demonstrating the actual CLAHE algorithm.
# =========================================================

print("\n==============================================")
print("          FAST PARAMETER SWEEP")
print("==============================================")


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


# =========================================================
# RUN PARAMETER COMBINATIONS
# =========================================================

for tile in tile_values:

    for clip in clip_values:

        # OpenCV optimized CLAHE
        clahe = cv2.createCLAHE(
            clipLimit=clip,
            tileGridSize=(
                tile,
                tile
            )
        )

        # Apply CLAHE
        result = clahe.apply(
            img
        )

        # Calculate entropy
        ent = entropy(
            result
        )

        # Store result
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
    f"\n{'Tile Size':<15}"
    f"{'Clip Limit':<15}"
    f"{'Entropy':<15}"
)

print("-" * 45)


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


print("\n==============================================")
print("             BEST RESULT")
print("==============================================")


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
# CREATE BEST CLAHE IMAGE
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
# SAVE BEST RESULT
# =========================================================

cv2.imwrite(
    os.path.join(
        output_folder,
        "best_CLAHE_result.jpg"
    ),
    best_image
)


# =========================================================
# PLOT ENTROPY VS CLIP LIMIT
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
# DISPLAY BEST RESULT
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


# =========================================================
# FINAL MESSAGE
# =========================================================

print("\n==============================================")
print("             EXPERIMENT COMPLETE")
print("==============================================")

print(
    "\nAll important outputs are saved in:"
)

print(
    output_folder
)
