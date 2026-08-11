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
    print("Error loading image!")
    exit()


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
# FIRST-PRINCIPLES CLAHE
# =========================================================

def clahe_from_scratch(
    image,
    tile_rows=8,
    tile_cols=8,
    clip_limit=2.0
):

    image = image.astype(np.uint8)

    height, width = image.shape

    # Tile dimensions
    tile_height = height / tile_rows
    tile_width = width / tile_cols

    # Store mappings
    mappings = []

    # =====================================================
    # CALCULATE LOCAL HISTOGRAM AND MAPPING
    # =====================================================

    for tr in range(tile_rows):

        row_mappings = []

        for tc in range(tile_cols):

            y1 = int(tr * tile_height)
            y2 = int((tr + 1) * tile_height)

            x1 = int(tc * tile_width)
            x2 = int((tc + 1) * tile_width)

            tile = image[y1:y2, x1:x2]

            # Histogram
            hist = np.bincount(
                tile.ravel(),
                minlength=256
            ).astype(np.float64)

            # -------------------------------------------------
            # CLIP HISTOGRAM
            # -------------------------------------------------

            tile_area = tile.size

            clip_value = max(
                1,
                int(
                    clip_limit
                    * tile_area
                    / 256
                )
            )

            excess = 0

            for i in range(256):

                if hist[i] > clip_value:

                    excess += hist[i] - clip_value

                    hist[i] = clip_value

            # -------------------------------------------------
            # REDISTRIBUTE EXCESS
            # -------------------------------------------------

            redistribution = excess / 256

            hist += redistribution

            # -------------------------------------------------
            # CDF
            # -------------------------------------------------

            cdf = np.cumsum(hist)

            # Normalize CDF
            cdf_min = cdf[0]
            cdf_max = cdf[-1]

            if cdf_max != cdf_min:

                mapping = (
                    (cdf - cdf_min)
                    / (cdf_max - cdf_min)
                    * 255
                )

            else:

                mapping = np.arange(256)

            mapping = np.clip(
                mapping,
                0,
                255
            )

            row_mappings.append(mapping)

        mappings.append(row_mappings)


    # =====================================================
    # BILINEAR INTERPOLATION
    # =====================================================

    output = np.zeros_like(image)

    for y in range(height):

        for x in range(width):

            # Position in tile grid
            gy = y / tile_height - 0.5
            gx = x / tile_width - 0.5

            y0 = int(np.floor(gy))
            x0 = int(np.floor(gx))

            y1 = y0 + 1
            x1 = x0 + 1

            # Clamp tile indices
            y0 = max(0, min(tile_rows - 1, y0))
            y1 = max(0, min(tile_rows - 1, y1))

            x0 = max(0, min(tile_cols - 1, x0))
            x1 = max(0, min(tile_cols - 1, x1))

            # Fraction
            dy = gy - np.floor(gy)
            dx = gx - np.floor(gx)

            dy = np.clip(dy, 0, 1)
            dx = np.clip(dx, 0, 1)

            intensity = int(image[y, x])

            # Four neighboring mappings
            f00 = mappings[y0][x0][intensity]
            f01 = mappings[y0][x1][intensity]
            f10 = mappings[y1][x0][intensity]
            f11 = mappings[y1][x1][intensity]

            # Bilinear interpolation
            value = (
                (1 - dx) * (1 - dy) * f00
                + dx * (1 - dy) * f01
                + (1 - dx) * dy * f10
                + dx * dy * f11
            )

            output[y, x] = np.clip(
                value,
                0,
                255
            )

    return output.astype(np.uint8)
