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
# CREATE DIFFERENT EXPOSURES
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
# FIRST-PRINCIPLES HISTOGRAM MATCHING
# =========================================================

def histogram_matching(source, reference):

    # Histogram of source
    source_hist = np.bincount(
        source.ravel(),
        minlength=256
    )

    # Histogram of reference
    reference_hist = np.bincount(
        reference.ravel(),
        minlength=256
    )

    # Normalize histograms
    source_pdf = source_hist / source.size
    reference_pdf = reference_hist / reference.size

    # CDF
    source_cdf = np.cumsum(source_pdf)
    reference_cdf = np.cumsum(reference_pdf)

    # Mapping
    mapping = np.zeros(256, dtype=np.uint8)

    for source_intensity in range(256):

        source_value = source_cdf[source_intensity]

        # Find reference intensity with closest CDF
        difference = np.abs(
            reference_cdf - source_value
        )

        reference_intensity = np.argmin(
            difference
        )

        mapping[source_intensity] = reference_intensity

    # Apply transformation
    output = mapping[source]

    return output, source_cdf, reference_cdf, mapping


# =========================================================
# MATCH BOTH SOURCES
# =========================================================

matched1, cdf1, ref_cdf, map1 = histogram_matching(
    source1,
    reference
)

matched2, cdf2, ref_cdf, map2 = histogram_matching(
    source2,
    reference
)


# =========================================================
# SAVE OUTPUTS
# =========================================================

cv2.imwrite(
    os.path.join(output_folder, "reference.jpg"),
    reference
)

cv2.imwrite(
    os.path.join(output_folder, "dark_source.jpg"),
    source1
)

cv2.imwrite(
    os.path.join(output_folder, "bright_source.jpg"),
    source2
)

cv2.imwrite(
    os.path.join(output_folder, "matched_dark.jpg"),
    matched1
)

cv2.imwrite(
    os.path.join(output_folder, "matched_bright.jpg"),
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
# DISPLAY RESULTS
# =========================================================

plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.imshow(reference, cmap="gray")
plt.title("Reference")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.imshow(source1, cmap="gray")
plt.title("Dark Source")
plt.axis("off")

plt.subplot(2, 3, 3)
plt.imshow(matched1, cmap="gray")
plt.title("Matched Dark")
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(source2, cmap="gray")
plt.title("Bright Source")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.imshow(matched2, cmap="gray")
plt.title("Matched Bright")
plt.axis("off")

plt.subplot(2, 3, 6)
plt.imshow(reference, cmap="gray")
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
# CDF COMPARISON
# =========================================================

def calculate_cdf(image):

    hist = get_histogram(image)

    pdf = hist / image.size

    return np.cumsum(pdf)


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
