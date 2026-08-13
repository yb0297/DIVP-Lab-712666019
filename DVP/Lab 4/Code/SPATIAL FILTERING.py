# ============================================================
# LAB: SPATIAL FILTERING
# Restoring and Enhancing Degraded Onboard Camera Feed
# for an Autonomous Ground Vehicle (AGV)
#
# COMPLETE JUPYTER NOTEBOOK VERSION
#
# Input:
# C:\Users\yoges\Downloads\Cloudhoppers.jpg
#
# All outputs:
# C:\Users\yoges\Downloads\AGV_Spatial_Filtering_Output
#
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 2. PATH SETUP
# ============================================================

INPUT_IMAGE = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"

OUTPUT_FOLDER = (
    r"C:\Users\yoges\Downloads"
    r"\AGV_Spatial_Filtering_Output"
)


# Output subfolders

DEGRADED_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "01_Degraded"
)

TASK1_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "02_Task1_Averaging"
)

TASK2_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "03_Task2_Laplacian"
)

TASK3_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "04_Task3_HighBoost"
)

GRID_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "05_Grids"
)

RESULT_FOLDER = os.path.join(
    OUTPUT_FOLDER,
    "06_Results"
)


# Create folders

folders = [
    OUTPUT_FOLDER,
    DEGRADED_FOLDER,
    TASK1_FOLDER,
    TASK2_FOLDER,
    TASK3_FOLDER,
    GRID_FOLDER,
    RESULT_FOLDER
]

for folder in folders:
    os.makedirs(
        folder,
        exist_ok=True
    )


print("=" * 70)
print("AGV SPATIAL FILTERING LAB")
print("=" * 70)

print("\nInput image:")
print(INPUT_IMAGE)

print("\nOutput folder:")
print(OUTPUT_FOLDER)


# ============================================================
# 3. CHECK INPUT IMAGE
# ============================================================

if not os.path.exists(INPUT_IMAGE):

    raise FileNotFoundError(
        "\nInput image was not found:\n"
        + INPUT_IMAGE
    )


# ============================================================
# 4. IMAGE SAVING FUNCTION
# ============================================================

def save_image(
    filename,
    image
):

    image = np.clip(
        image,
        0,
        255
    ).astype(
        np.uint8
    )

    success = cv2.imwrite(
        filename,
        image
    )

    if not success:

        print(
            "WARNING: Could not save:",
            filename
        )


# ============================================================
# 5. NORMALIZE IMAGE
# ============================================================

def normalize_image(image):

    minimum = np.min(
        image
    )

    maximum = np.max(
        image
    )

    if maximum == minimum:

        return np.zeros_like(
            image,
            dtype=np.uint8
        )

    normalized = (
        (image - minimum)
        /
        (maximum - minimum)
        *
        255
    )

    return normalized.astype(
        np.uint8
    )


# ============================================================
# 6. LOAD IMAGE
# ============================================================

print("\nLoading image...")

image = cv2.imread(
    INPUT_IMAGE,
    cv2.IMREAD_GRAYSCALE
)


if image is None:

    raise ValueError(
        "OpenCV could not read the image."
    )


print(
    "Original image size:",
    image.shape
)


# ============================================================
# 7. RESIZE FOR PRACTICAL EXECUTION
# ============================================================
#
# From-scratch filtering uses Python loops.
# Very large images would take too long.
#
# Maximum width = 700 pixels
#
# ============================================================

MAX_WIDTH = 700


original_height, original_width = (
    image.shape
)


if original_width > MAX_WIDTH:

    scale = (
        MAX_WIDTH
        /
        original_width
    )

    new_width = MAX_WIDTH

    new_height = int(
        original_height
        *
        scale
    )

    image = cv2.resize(
        image,
        (
            new_width,
            new_height
        ),
        interpolation=cv2.INTER_AREA
    )


print(
    "Working image size:",
    image.shape
)


# Convert to floating point

clean = image.astype(
    np.float64
)


# ============================================================
# 8. SAVE CLEAN GROUND TRUTH
# ============================================================

save_image(
    os.path.join(
        DEGRADED_FOLDER,
        "00_clean_ground_truth.png"
    ),
    clean
)


# ============================================================
# 9. CORRELATION FROM SCRATCH
# ============================================================

def correlate2d(
    image,
    kernel
):

    """
    2-D spatial correlation implemented
    from first principles.

    No:
        cv2.filter2D()
        scipy.signal
    """

    image = image.astype(
        np.float64
    )

    kernel = kernel.astype(
        np.float64
    )

    image_height = image.shape[0]
    image_width = image.shape[1]

    kernel_height = kernel.shape[0]
    kernel_width = kernel.shape[1]

    pad_height = (
        kernel_height // 2
    )

    pad_width = (
        kernel_width // 2
    )

    # Edge padding

    padded = np.pad(
        image,
        (
            (
                pad_height,
                pad_height
            ),
            (
                pad_width,
                pad_width
            )
        ),
        mode="edge"
    )

    output = np.zeros(
        (
            image_height,
            image_width
        ),
        dtype=np.float64
    )


    # Pixel-by-pixel correlation

    for i in range(
        image_height
    ):

        for j in range(
            image_width
        ):

            region = padded[
                i:i + kernel_height,
                j:j + kernel_width
            ]

            output[i, j] = np.sum(
                region * kernel
            )


    return output


# ============================================================
# 10. CONVOLUTION FROM SCRATCH
# ============================================================

def convolve2d(
    image,
    kernel
):

    """
    True convolution.

    Convolution flips the kernel
    by 180 degrees before correlation.
    """

    flipped_kernel = np.flip(
        kernel
    )

    return correlate2d(
        image,
        flipped_kernel
    )


# ============================================================
# 11. AVERAGING FILTER
# ============================================================

def averaging_filter(
    image,
    size
):

    kernel = np.ones(
        (
            size,
            size
        ),
        dtype=np.float64
    )

    kernel = (
        kernel
        /
        (size * size)
    )

    result = correlate2d(
        image,
        kernel
    )

    return result


# ============================================================
# 12. GAUSSIAN NOISE
# ============================================================

def add_gaussian_noise(
    image,
    sigma,
    seed=42
):

    rng = np.random.default_rng(
        seed
    )

    noise = rng.normal(
        0,
        sigma,
        image.shape
    )

    noisy = (
        image
        +
        noise
    )

    return np.clip(
        noisy,
        0,
        255
    )


# ============================================================
# 13. MOTION BLUR KERNEL
# ============================================================

def create_motion_kernel(
    length=9
):

    kernel = np.zeros(
        (
            length,
            length
        ),
        dtype=np.float64
    )

    center = (
        length // 2
    )

    kernel[
        center,
        :
    ] = (
        1.0
        /
        length
    )

    return kernel


# ============================================================
# 14. LAPLACIAN KERNELS
# ============================================================

LAPLACIAN_4 = np.array(
    [
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ],
    dtype=np.float64
)


LAPLACIAN_8 = np.array(
    [
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ],
    dtype=np.float64
)


# ============================================================
# 15. LAPLACIAN SHARPENING
# ============================================================

def laplacian_sharpen(
    image,
    kernel
):

    response = correlate2d(
        image,
        kernel
    )

    sharpened = (
        image
        +
        response
    )

    return np.clip(
        sharpened,
        0,
        255
    )


# ============================================================
# 16. HIGH-BOOST FILTER
# ============================================================

def high_boost(
    image,
    k,
    blur_size=5
):

    blurred = averaging_filter(
        image,
        blur_size
    )

    mask = (
        image
        -
        blurred
    )

    result = (
        image
        +
        k * mask
    )

    return np.clip(
        result,
        0,
        255
    )


# ============================================================
# 17. PSNR
# ============================================================

def calculate_psnr(
    original,
    processed
):

    original = original.astype(
        np.float64
    )

    processed = processed.astype(
        np.float64
    )

    mse = np.mean(
        (
            original
            -
            processed
        ) ** 2
    )

    if mse == 0:

        return float("inf")

    return (
        10
        *
        np.log10(
            (255.0 ** 2)
            /
            mse
        )
    )


# ============================================================
# 18. SHARPNESS METRIC
# ============================================================

def calculate_sharpness(
    image
):

    """
    Sharpness metric:

    Variance of Laplacian.

    Higher value means stronger
    high-frequency content.

    Note:
    Noise can also increase this value.
    """

    response = correlate2d(
        image,
        LAPLACIAN_4
    )

    return float(
        np.var(response)
    )


# ============================================================
# 19. GRID SAVING FUNCTION
# ============================================================

def save_grid(
    images,
    titles,
    filename,
    columns=3
):

    count = len(
        images
    )

    rows = int(
        np.ceil(
            count / columns
        )
    )

    fig, axes = plt.subplots(
        rows,
        columns,
        figsize=(
            5 * columns,
            4 * rows
        )
    )

    axes = np.atleast_1d(
        axes
    ).flatten()


    for i in range(count):

        axes[i].imshow(
            images[i],
            cmap="gray",
            vmin=0,
            vmax=255
        )

        axes[i].set_title(
            titles[i]
        )

        axes[i].axis(
            "off"
        )


    for i in range(
        count,
        len(axes)
    ):

        axes[i].axis(
            "off"
        )


    plt.tight_layout()

    plt.savefig(
        filename,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# TASK 0
# GENERATE DEGRADED IMAGES
# ============================================================

print("\n")
print("=" * 70)
print("TASK 0 - GENERATING DEGRADED IMAGES")
print("=" * 70)


# ------------------------------------------------------------
# Gaussian noise sigma = 10
# ------------------------------------------------------------

print(
    "\nGenerating Gaussian noise: sigma = 10"
)

noisy_10 = add_gaussian_noise(
    clean,
    sigma=10,
    seed=42
)


# ------------------------------------------------------------
# Gaussian noise sigma = 25
# ------------------------------------------------------------

print(
    "Generating Gaussian noise: sigma = 25"
)

noisy_25 = add_gaussian_noise(
    clean,
    sigma=25,
    seed=42
)


# ------------------------------------------------------------
# Motion blur
# ------------------------------------------------------------

print(
    "Generating motion blur: length = 9"
)

motion_kernel = create_motion_kernel(
    length=9
)

motion_blurred = correlate2d(
    clean,
    motion_kernel
)


# Save degraded images

save_image(
    os.path.join(
        DEGRADED_FOLDER,
        "01_noisy_sigma_10.png"
    ),
    noisy_10
)


save_image(
    os.path.join(
        DEGRADED_FOLDER,
        "02_noisy_sigma_25.png"
    ),
    noisy_25
)


save_image(
    os.path.join(
        DEGRADED_FOLDER,
        "03_motion_blur_length_9.png"
    ),
    motion_blurred
)


# Save degradation grid

save_grid(
    [
        clean,
        noisy_10,
        noisy_25,
        motion_blurred
    ],
    [
        "Clean Ground Truth",
        "Gaussian Noise σ = 10",
        "Gaussian Noise σ = 25",
        "Motion Blur Length = 9"
    ],
    os.path.join(
        GRID_FOLDER,
        "00_Degraded_Images.png"
    ),
    columns=2
)


# ============================================================
# RESULT STORAGE
# ============================================================

all_results = []


# ============================================================
# TASK 1
# NOISE SUPPRESSION VIA AVERAGING
# ============================================================

print("\n")
print("=" * 70)
print("TASK 1 - NOISE SUPPRESSION VIA AVERAGING")
print("=" * 70)


task1_images = []
task1_titles = []


for sigma, noisy_image in [

    (10, noisy_10),

    (25, noisy_25)

]:

    for kernel_size in [

        3,
        5,
        9

    ]:

        print(
            f"\nProcessing σ={sigma}, "
            f"kernel={kernel_size}x{kernel_size}"
        )


        result = averaging_filter(
            noisy_image,
            kernel_size
        )


        filename = os.path.join(
            TASK1_FOLDER,
            f"sigma_{sigma}_"
            f"kernel_{kernel_size}x"
            f"{kernel_size}.png"
        )


        save_image(
            filename,
            result
        )


        psnr = calculate_psnr(
            clean,
            result
        )


        sharpness = calculate_sharpness(
            result
        )


        all_results.append(
            {
                "Task":
                    "Task 1 - Averaging",

                "Noise":
                    f"sigma={sigma}",

                "Parameter":
                    f"{kernel_size}x"
                    f"{kernel_size}",

                "PSNR_dB":
                    psnr,

                "Sharpness":
                    sharpness
            }
        )


        task1_images.append(
            result
        )


        task1_titles.append(
            f"σ={sigma}, "
            f"{kernel_size}x"
            f"{kernel_size}"
        )


# Save Task 1 grid

save_grid(
    task1_images,
    task1_titles,
    os.path.join(
        GRID_FOLDER,
        "01_Task1_Averaging.png"
    ),
    columns=3
)


# ============================================================
# TASK 2
# LAPLACIAN SHARPENING
# ============================================================

print("\n")
print("=" * 70)
print("TASK 2 - LAPLACIAN SHARPENING")
print("=" * 70)


# ------------------------------------------------------------
# 4-neighbor
# ------------------------------------------------------------

print(
    "\nApplying 4-neighbor Laplacian..."
)

laplacian_response_4 = correlate2d(
    motion_blurred,
    LAPLACIAN_4
)


laplacian_sharp_4 = (
    motion_blurred
    +
    laplacian_response_4
)


laplacian_sharp_4 = np.clip(
    laplacian_sharp_4,
    0,
    255
)


# ------------------------------------------------------------
# 8-neighbor
# ------------------------------------------------------------

print(
    "Applying 8-neighbor Laplacian..."
)

laplacian_response_8 = correlate2d(
    motion_blurred,
    LAPLACIAN_8
)


laplacian_sharp_8 = (
    motion_blurred
    +
    laplacian_response_8
)


laplacian_sharp_8 = np.clip(
    laplacian_sharp_8,
    0,
    255
)


# Save response maps

save_image(
    os.path.join(
        TASK2_FOLDER,
        "01_4_neighbor_response.png"
    ),
    normalize_image(
        laplacian_response_4
    )
)


save_image(
    os.path.join(
        TASK2_FOLDER,
        "02_8_neighbor_response.png"
    ),
    normalize_image(
        laplacian_response_8
    )
)


# Save sharpened outputs

save_image(
    os.path.join(
        TASK2_FOLDER,
        "03_4_neighbor_sharpened.png"
    ),
    laplacian_sharp_4
)


save_image(
    os.path.join(
        TASK2_FOLDER,
        "04_8_neighbor_sharpened.png"
    ),
    laplacian_sharp_8
)


# Metrics

all_results.append(
    {
        "Task":
            "Task 2 - Laplacian",

        "Noise":
            "Motion Blur",

        "Parameter":
            "4-neighbor",

        "PSNR_dB":
            calculate_psnr(
                clean,
                laplacian_sharp_4
            ),

        "Sharpness":
            calculate_sharpness(
                laplacian_sharp_4
            )
    }
)


all_results.append(
    {
        "Task":
            "Task 2 - Laplacian",

        "Noise":
            "Motion Blur",

        "Parameter":
            "8-neighbor",

        "PSNR_dB":
            calculate_psnr(
                clean,
                laplacian_sharp_8
            ),

        "Sharpness":
            calculate_sharpness(
                laplacian_sharp_8
            )
    }
)


# Save Task 2 grid

save_grid(
    [
        motion_blurred,

        normalize_image(
            laplacian_response_4
        ),

        normalize_image(
            laplacian_response_8
        ),

        laplacian_sharp_4,

        laplacian_sharp_8
    ],

    [
        "Motion Blurred",

        "4-Neighbor Response",

        "8-Neighbor Response",

        "4-Neighbor Sharpened",

        "8-Neighbor Sharpened"
    ],

    os.path.join(
        GRID_FOLDER,
        "02_Task2_Laplacian.png"
    ),

    columns=3
)


# ============================================================
# TASK 3
# UNSHARP MASKING / HIGH-BOOST
# ============================================================

print("\n")
print("=" * 70)
print("TASK 3 - UNSHARP MASKING / HIGH-BOOST")
print("=" * 70)


task3_images = []
task3_titles = []


k_values = [
    1.0,
    1.5,
    2.0,
    3.0
]


for k in k_values:

    print(
        f"\nProcessing k = {k}"
    )


    result = high_boost(
        noisy_10,
        k=k,
        blur_size=5
    )


    filename = os.path.join(
        TASK3_FOLDER,
        f"highboost_k_{k}.png"
    )


    save_image(
        filename,
        result
    )


    psnr = calculate_psnr(
        clean,
        result
    )


    sharpness = calculate_sharpness(
        result
    )


    all_results.append(
        {
            "Task":
                "Task 3 - High Boost",

            "Noise":
                "sigma=10",

            "Parameter":
                f"k={k}",

            "PSNR_dB":
                psnr,

            "Sharpness":
                sharpness
        }
    )


    task3_images.append(
        result
    )


    task3_titles.append(
        f"k = {k}"
    )


# Save Task 3 grid

save_grid(
    task3_images,
    task3_titles,
    os.path.join(
        GRID_FOLDER,
        "03_Task3_HighBoost.png"
    ),
    columns=4
)


# ============================================================
# TASK 3 - METRIC GRAPHS
# ============================================================

sharpness_values = []
psnr_values = []


for k in k_values:

    result = high_boost(
        noisy_10,
        k=k,
        blur_size=5
    )


    sharpness_values.append(
        calculate_sharpness(
            result
        )
    )


    psnr_values.append(
        calculate_psnr(
            clean,
            result
        )
    )


# ------------------------------------------------------------
# Sharpness vs k
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    k_values,
    sharpness_values,
    marker="o"
)

plt.xlabel(
    "Boost Factor (k)"
)

plt.ylabel(
    "Variance of Laplacian"
)

plt.title(
    "Sharpness vs Boost Factor"
)

plt.grid(
    True
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRID_FOLDER,
        "04_Sharpness_vs_k.png"
    ),
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# PSNR vs k
# ------------------------------------------------------------

plt.figure(
    figsize=(8, 5)
)

plt.plot(
    k_values,
    psnr_values,
    marker="o"
)

plt.xlabel(
    "Boost Factor (k)"
)

plt.ylabel(
    "PSNR (dB)"
)

plt.title(
    "PSNR vs Boost Factor"
)

plt.grid(
    True
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        GRID_FOLDER,
        "05_PSNR_vs_k.png"
    ),
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# TASK 4
# OBJECTIVE EVALUATION
# ============================================================

print("\n")
print("=" * 70)
print("TASK 4 - OBJECTIVE EVALUATION")
print("=" * 70)


results_df = pd.DataFrame(
    all_results
)


results_df[
    "PSNR_dB"
] = results_df[
    "PSNR_dB"
].round(4)


results_df[
    "Sharpness"
] = results_df[
    "Sharpness"
].round(4)


# ------------------------------------------------------------
# Print table
# ------------------------------------------------------------

print(
    "\nRESULT TABLE\n"
)

print(
    results_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Save CSV
# ------------------------------------------------------------

results_df.to_csv(
    os.path.join(
        RESULT_FOLDER,
        "metrics_results.csv"
    ),
    index=False
)


# ------------------------------------------------------------
# Save Excel
# ------------------------------------------------------------

results_df.to_excel(
    os.path.join(
        RESULT_FOLDER,
        "metrics_results.xlsx"
    ),
    index=False
)


# ============================================================
# TASK 5
# PIPELINE RECOMMENDATION TEST
# ============================================================

print("\n")
print("=" * 70)
print("TASK 5 - PIPELINE COMPARISON")
print("=" * 70)


# ------------------------------------------------------------
# Pipeline A:
# DENOISE -> SHARPEN
# ------------------------------------------------------------

print(
    "\nPipeline A:"
)

print(
    "Denoise -> Sharpen"
)


denoised_first = averaging_filter(
    noisy_10,
    5
)


pipeline_a = high_boost(
    denoised_first,
    k=1.5,
    blur_size=5
)


# ------------------------------------------------------------
# Pipeline B:
# SHARPEN -> DENOISE
# ------------------------------------------------------------

print(
    "\nPipeline B:"
)

print(
    "Sharpen -> Denoise"
)


sharpened_first = high_boost(
    noisy_10,
    k=1.5,
    blur_size=5
)


pipeline_b = averaging_filter(
    sharpened_first,
    5
)


# ------------------------------------------------------------
# Calculate metrics
# ------------------------------------------------------------

pipeline_results = pd.DataFrame(
    [

        {
            "Pipeline":
                "Denoise -> Sharpen",

            "PSNR_dB":
                calculate_psnr(
                    clean,
                    pipeline_a
                ),

            "Sharpness":
                calculate_sharpness(
                    pipeline_a
                )
        },

        {
            "Pipeline":
                "Sharpen -> Denoise",

            "PSNR_dB":
                calculate_psnr(
                    clean,
                    pipeline_b
                ),

            "Sharpness":
                calculate_sharpness(
                    pipeline_b
                )
        }

    ]
)


pipeline_results[
    "PSNR_dB"
] = pipeline_results[
    "PSNR_dB"
].round(4)


pipeline_results[
    "Sharpness"
] = pipeline_results[
    "Sharpness"
].round(4)


print(
    "\nPipeline comparison:"
)

print(
    pipeline_results.to_string(
        index=False
    )
)


# Save pipeline CSV

pipeline_results.to_csv(
    os.path.join(
        RESULT_FOLDER,
        "pipeline_order_comparison.csv"
    ),
    index=False
)


# Save final recommended pipeline

save_image(
    os.path.join(
        RESULT_FOLDER,
        "final_pipeline_output.png"
    ),
    pipeline_a
)


# Save comparison grid

save_grid(
    [
        noisy_10,
        pipeline_a,
        pipeline_b
    ],

    [
        "Original Noisy σ=10",

        "Denoise → Sharpen",

        "Sharpen → Denoise"
    ],

    os.path.join(
        GRID_FOLDER,
        "06_Pipeline_Order.png"
    ),

    columns=3
)


# ============================================================
# REFLECTION QUESTION 4
# EXTRA HIGH-NOISE TEST
# ============================================================

print("\n")
print("=" * 70)
print("EXTRA NOISE TEST")
print("=" * 70)


extra_results = []


for sigma in [
    25,
    40,
    60,
    80
]:

    print(
        f"Testing sigma = {sigma}"
    )


    noisy = add_gaussian_noise(
        clean,
        sigma=sigma,
        seed=42
    )


    sharpened = high_boost(
        noisy,
        k=2.0,
        blur_size=5
    )


    save_image(
        os.path.join(
            RESULT_FOLDER,
            f"extra_noise_sigma_{sigma}.png"
        ),
        sharpened
    )


    extra_results.append(
        {
            "Sigma":
                sigma,

            "PSNR_dB":
                calculate_psnr(
                    clean,
                    sharpened
                ),

            "Sharpness":
                calculate_sharpness(
                    sharpened
                )
        }
    )


extra_df = pd.DataFrame(
    extra_results
)


extra_df[
    "PSNR_dB"
] = extra_df[
    "PSNR_dB"
].round(4)


extra_df[
    "Sharpness"
] = extra_df[
    "Sharpness"
].round(4)


extra_df.to_csv(
    os.path.join(
        RESULT_FOLDER,
        "extra_noise_results.csv"
    ),
    index=False
)


# ============================================================
# BEST CONFIGURATIONS
# ============================================================

best_psnr_index = (
    results_df[
        "PSNR_dB"
    ].idxmax()
)


best_sharpness_index = (
    results_df[
        "Sharpness"
    ].idxmax()
)


best_psnr = (
    results_df.loc[
        best_psnr_index
    ]
)


best_sharpness = (
    results_df.loc[
        best_sharpness_index
    ]
)


# ============================================================
# AUTOMATIC EXPERIMENT SUMMARY
# ============================================================

summary = f"""

============================================================
AGV SPATIAL FILTERING LAB
EXPERIMENT SUMMARY
============================================================

INPUT IMAGE
------------------------------------------------------------

{INPUT_IMAGE}

Working image size:
{clean.shape}


TASK 0 - IMAGE DEGRADATION
------------------------------------------------------------

Gaussian noise:
    sigma = 10
    sigma = 25

Motion blur:
    Linear horizontal motion blur
    Kernel length = 9 pixels


TASK 1 - AVERAGING FILTER
------------------------------------------------------------

Kernel sizes:
    3 x 3
    5 x 5
    9 x 9

The averaging filter suppresses random noise by replacing
each pixel with the local average.

As kernel size increases:
    - noise suppression generally increases
    - fine details are increasingly blurred
    - navigation-relevant edges can become weaker


TASK 2 - LAPLACIAN SHARPENING
------------------------------------------------------------

4-neighbor Laplacian:

[ 0 -1  0 ]
[-1  4 -1 ]
[ 0 -1  0 ]

8-neighbor Laplacian:

[-1 -1 -1]
[-1  8 -1]
[-1 -1 -1]

The 4-neighbor version mainly responds to horizontal and
vertical neighboring intensity changes.

The 8-neighbor version also includes diagonal neighbors,
making it sensitive to diagonal structures.


TASK 3 - UNSHARP MASKING / HIGH-BOOST
------------------------------------------------------------

Boost factors tested:

    k = 1.0
    k = 1.5
    k = 2.0
    k = 3.0

The high-boost operation was:

    g(x,y) = f(x,y) + k[f(x,y) - f_blurred(x,y)]

Increasing k strengthens high-frequency components.

However, excessive k can also amplify noise.


TASK 4 - OBJECTIVE METRICS
------------------------------------------------------------

PSNR:
Peak Signal-to-Noise Ratio.

Higher PSNR indicates lower pixel-wise error relative
to the clean ground-truth image.

Sharpness:
Variance of the 4-neighbor Laplacian response.

Higher sharpness indicates stronger high-frequency
components. However, noise can also increase this metric.


BEST PSNR CONFIGURATION
------------------------------------------------------------

Task:
{best_psnr["Task"]}

Noise:
{best_psnr["Noise"]}

Parameter:
{best_psnr["Parameter"]}

PSNR:
{best_psnr["PSNR_dB"]:.4f} dB

Sharpness:
{best_psnr["Sharpness"]:.4f}


HIGHEST SHARPNESS CONFIGURATION
------------------------------------------------------------

Task:
{best_sharpness["Task"]}

Noise:
{best_sharpness["Noise"]}

Parameter:
{best_sharpness["Parameter"]}

PSNR:
{best_sharpness["PSNR_dB"]:.4f} dB

Sharpness:
{best_sharpness["Sharpness"]:.4f}


TASK 5 - PIPELINE
------------------------------------------------------------

Recommended starting pipeline:

    Gaussian-noisy input
             |
             v
       5 x 5 Averaging
             |
             v
       High-Boost k=1.5
             |
             v
       Enhanced image


The final choice should consider both PSNR and sharpness,
because maximizing sharpness alone can amplify noise.


PIPELINE ORDER COMPARISON
------------------------------------------------------------

Denoise -> Sharpen:

PSNR:
{pipeline_results.iloc[0]["PSNR_dB"]:.4f} dB

Sharpness:
{pipeline_results.iloc[0]["Sharpness"]:.4f}


Sharpen -> Denoise:

PSNR:
{pipeline_results.iloc[1]["PSNR_dB"]:.4f} dB

Sharpness:
{pipeline_results.iloc[1]["Sharpness"]:.4f}


REFLECTION QUESTION 4
------------------------------------------------------------

Additional noise levels tested:

sigma = 25
sigma = 40
sigma = 60
sigma = 80

The results are stored in:

extra_noise_results.csv


OUTPUT LOCATION
------------------------------------------------------------

All experiment files are stored in:

{OUTPUT_FOLDER}


============================================================
END OF EXPERIMENT SUMMARY
============================================================
"""


# Save summary

with open(
    os.path.join(
        RESULT_FOLDER,
        "experiment_summary.txt"
    ),
    "w",
    encoding="utf-8"
) as file:

    file.write(
        summary
    )


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n")
print("=" * 70)
print("EXPERIMENT COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\nALL OUTPUT FILES HAVE BEEN SAVED TO:"
)

print(
    OUTPUT_FOLDER
)

print("\nFolders created:")

print(
    "01_Degraded"
)

print(
    "02_Task1_Averaging"
)

print(
    "03_Task2_Laplacian"
)

print(
    "04_Task3_HighBoost"
)

print(
    "05_Grids"
)

print(
    "06_Results"
)

print("\nImportant result files:")

print(
    "metrics_results.csv"
)

print(
    "metrics_results.xlsx"
)

print(
    "pipeline_order_comparison.csv"
)

print(
    "extra_noise_results.csv"
)

print(
    "experiment_summary.txt"
)

print("\nEXPERIMENT FINISHED.")
