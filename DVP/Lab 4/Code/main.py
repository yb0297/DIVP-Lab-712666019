"""
AGV Spatial Filtering Lab
All spatial filters are implemented from scratch.

Input:
    C:\Users\yoges\Downloads\Cloudhoppers.jpg

Run:
    python src\main.py

The script creates:
    outputs/degraded/
    outputs/task1/
    outputs/task2/
    outputs/task3/
    outputs/tables/
    outputs/figures/

Only image I/O, plotting and CSV writing use OpenCV/matplotlib/pandas.
No cv2.filter2D, cv2.blur, scipy.signal, skimage filters, etc. are used.
"""

import os
import csv
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_PATH = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(ROOT, "outputs")
DEGRADED_DIR = os.path.join(OUTPUT_DIR, "degraded")
TASK1_DIR = os.path.join(OUTPUT_DIR, "task1")
TASK2_DIR = os.path.join(OUTPUT_DIR, "task2")
TASK3_DIR = os.path.join(OUTPUT_DIR, "task3")
TABLE_DIR = os.path.join(OUTPUT_DIR, "tables")
FIG_DIR = os.path.join(OUTPUT_DIR, "figures")

for d in [DEGRADED_DIR, TASK1_DIR, TASK2_DIR, TASK3_DIR, TABLE_DIR, FIG_DIR]:
    os.makedirs(d, exist_ok=True)

RNG = np.random.default_rng(42)


# ============================================================
# BASIC UTILITIES
# ============================================================

def save_image(path, image):
    image = np.clip(image, 0, 255).astype(np.uint8)
    cv2.imwrite(path, image)


def normalize_to_uint8(image):
    image = image.astype(np.float32)
    mn, mx = image.min(), image.max()
    if mx - mn < 1e-12:
        return np.zeros_like(image, dtype=np.uint8)
    out = (image - mn) * 255.0 / (mx - mn)
    return np.clip(out, 0, 255).astype(np.uint8)


def psnr(reference, test):
    """PSNR in dB against the clean ground truth."""
    ref = reference.astype(np.float64)
    tst = test.astype(np.float64)
    mse = np.mean((ref - tst) ** 2)
    if mse == 0:
        return float("inf")
    return 10.0 * math.log10((255.0 ** 2) / mse)


def laplacian_variance(image):
    """
    Sharpness metric:
    variance of the 4-neighbor Laplacian response.

    Larger values mean more high-frequency/edge energy, but
    very large values can also indicate amplified noise.
    """
    kernel = np.array([
        [0,  1, 0],
        [1, -4, 1],
        [0,  1, 0]
    ], dtype=np.float32)
    response = correlate2d(image.astype(np.float32), kernel)
    return float(np.var(response))


def mean_gradient_magnitude(image):
    """Alternative edge-strength metric."""
    img = image.astype(np.float32)
    gx = np.zeros_like(img)
    gy = np.zeros_like(img)
    gx[:, 1:-1] = (img[:, 2:] - img[:, :-2]) / 2.0
    gy[1:-1, :] = (img[2:, :] - img[:-2, :]) / 2.0
    return float(np.mean(np.sqrt(gx * gx + gy * gy)))


# ============================================================
# FROM-SCRATCH 2D CORRELATION
# ============================================================

def pad_image(image, pad_h, pad_w, mode="reflect"):
    """
    Padding implemented using NumPy padding.
    The filtering operation itself is implemented manually.
    """
    return np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode=mode)


def correlate2d(image, kernel):
    """
    2D spatial correlation from first principles.

    Correlation:
        g(x,y) = sum_i sum_j f(x+i,y+j) h(i,j)

    No cv2.filter2D or scipy.signal is used.
    """
    image = image.astype(np.float32)
    kernel = np.asarray(kernel, dtype=np.float32)

    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2

    padded = pad_image(image, ph, pw, mode="reflect")
    output = np.zeros_like(image, dtype=np.float32)

    # Vectorized row/column accumulation.
    # This is still explicit spatial correlation.
    for i in range(kh):
        for j in range(kw):
            output += kernel[i, j] * padded[i:i + image.shape[0],
                                            j:j + image.shape[1]]

    return output


def convolve2d(image, kernel):
    """
    True convolution = correlation with a 180-degree flipped kernel.
    """
    kernel = np.asarray(kernel)
    flipped = np.flip(kernel, axis=(0, 1))
    return correlate2d(image, flipped)


# ============================================================
# TASK 1: AVERAGING FILTER
# ============================================================

def averaging_filter(image, size):
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    return correlate2d(image, kernel)


# ============================================================
# DEGRADATION MODELS
# ============================================================

def add_gaussian_noise(image, sigma, rng=RNG):
    noise = rng.normal(0.0, sigma, image.shape)
    noisy = image.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def motion_blur(image, length=9):
    """
    Mild horizontal linear motion blur.

    The blur is generated manually using our own convolution.
    """
    kernel = np.zeros((length, length), dtype=np.float32)
    kernel[length // 2, :] = 1.0 / length
    return np.clip(convolve2d(image, kernel), 0, 255).astype(np.uint8)


# ============================================================
# TASK 2: LAPLACIAN SHARPENING
# ============================================================

LAPLACIAN_4 = np.array([
    [0,  1, 0],
    [1, -4, 1],
    [0,  1, 0]
], dtype=np.float32)

LAPLACIAN_8 = np.array([
    [1,  1, 1],
    [1, -8, 1],
    [1,  1, 1]
], dtype=np.float32)


def laplacian_response(image, variant=4):
    kernel = LAPLACIAN_4 if variant == 4 else LAPLACIAN_8
    return correlate2d(image, kernel)


def laplacian_sharpen(image, variant=4, amount=1.0):
    """
    f_sharp = f - amount * Laplacian(f)

    The sign follows the kernels used above.
    """
    response = laplacian_response(image, variant)
    sharpened = image.astype(np.float32) - amount * response
    return np.clip(sharpened, 0, 255).astype(np.uint8)


# ============================================================
# TASK 3: UNSHARP MASK / HIGH BOOST
# ============================================================

def gaussian_kernel(size=5, sigma=1.0):
    """
    Gaussian kernel generated from the analytical Gaussian equation.
    """
    ax = np.arange(-(size // 2), size // 2 + 1, dtype=np.float32)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx * xx + yy * yy) / (2 * sigma * sigma))
    kernel /= np.sum(kernel)
    return kernel.astype(np.float32)


def unsharp_highboost(image, k=1.0, blur_size=5, blur_sigma=1.0):
    """
    g = f + k(f - f_blur)

    k=1   -> unsharp masking
    k>1   -> high-boost filtering
    """
    kernel = gaussian_kernel(blur_size, blur_sigma)
    blurred = correlate2d(image, kernel)
    mask = image.astype(np.float32) - blurred
    result = image.astype(np.float32) + k * mask
    return np.clip(result, 0, 255).astype(np.uint8)


# ============================================================
# PLOTTING
# ============================================================

def save_grid(images, titles, filename, cols=3, figsize=(15, 9)):
    rows = math.ceil(len(images) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = np.array(axes).reshape(-1)

    for ax, image, title in zip(axes, images, titles):
        ax.imshow(image, cmap="gray", vmin=0, vmax=255)
        ax.set_title(title)
        ax.axis("off")

    for ax in axes[len(images):]:
        ax.axis("off")

    fig.tight_layout()
    fig.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_sharpness_curve(k_values, sharpness_values, filename):
    plt.figure(figsize=(7, 5))
    plt.plot(k_values, sharpness_values, marker="o")
    plt.xlabel("Boost factor k")
    plt.ylabel("Variance of Laplacian")
    plt.title("Task 3: Sharpness vs Boost Factor")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


def plot_metric_comparison(rows, filename):
    labels = [r["configuration"] for r in rows]
    psnrs = [r["psnr_db"] for r in rows]

    plt.figure(figsize=(max(10, len(labels) * 0.55), 6))
    plt.bar(np.arange(len(labels)), psnrs)
    plt.xticks(np.arange(len(labels)), labels, rotation=70, ha="right")
    plt.ylabel("PSNR (dB)")
    plt.title("PSNR Comparison")
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()


# ============================================================
# CSV REPORTING
# ============================================================

def write_csv(filename, rows):
    if not rows:
        return
    keys = list(rows[0].keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def main():
    print("=" * 70)
    print("AGV SPATIAL FILTERING LAB")
    print("=" * 70)

    # --------------------------------------------------------
    # Load image
    # --------------------------------------------------------
    if not os.path.exists(INPUT_PATH):
        print("\nINPUT IMAGE NOT FOUND")
        print("Expected:")
        print(INPUT_PATH)
        print("\nIf using another computer, edit INPUT_PATH in main.py.")
        return

    color = cv2.imread(INPUT_PATH, cv2.IMREAD_COLOR)
    if color is None:
        raise RuntimeError("Could not read input image.")

    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

    # Resize only if extremely large, to keep from-scratch processing practical.
    max_dimension = 1000
    scale = min(1.0, max_dimension / max(gray.shape))
    if scale < 1.0:
        gray = cv2.resize(
            gray,
            (int(gray.shape[1] * scale), int(gray.shape[0] * scale)),
            interpolation=cv2.INTER_AREA
        )

    save_image(os.path.join(DEGRADED_DIR, "clean_ground_truth.png"), gray)

    # --------------------------------------------------------
    # Generate degraded data
    # --------------------------------------------------------
    noisy10 = add_gaussian_noise(gray, 10)
    noisy25 = add_gaussian_noise(gray, 25)
    blurred = motion_blur(gray, length=9)

    save_image(os.path.join(DEGRADED_DIR, "noisy_sigma10.png"), noisy10)
    save_image(os.path.join(DEGRADED_DIR, "noisy_sigma25.png"), noisy25)
    save_image(os.path.join(DEGRADED_DIR, "motion_blur_length9.png"), blurred)

    save_grid(
        [gray, noisy10, noisy25, blurred],
        ["Clean Ground Truth", "Gaussian Noise σ=10",
         "Gaussian Noise σ=25", "Motion Blur L=9"],
        os.path.join(FIG_DIR, "degradation_overview.png"),
        cols=2
    )

    # --------------------------------------------------------
    # TASK 1
    # --------------------------------------------------------
    task1_rows = []
    task1_images = []
    task1_titles = []

    for sigma, source in [(10, noisy10), (25, noisy25)]:
        for size in [3, 5, 9]:
            result = averaging_filter(source, size)
            filename = f"avg_sigma{sigma}_kernel{size}.png"
            save_image(os.path.join(TASK1_DIR, filename), result)

            task1_images.append(result)
            task1_titles.append(f"σ={sigma}, {size}×{size}")

            task1_rows.append({
                "task": "Task 1",
                "configuration": f"Average {size}x{size}, sigma={sigma}",
                "noise_sigma": sigma,
                "kernel_size": size,
                "parameter": size,
                "psnr_db": round(psnr(gray, result), 4),
                "sharpness_variance_laplacian": round(laplacian_variance(result), 4),
                "mean_gradient_magnitude": round(mean_gradient_magnitude(result), 4)
            })

    save_grid(
        task1_images,
        task1_titles,
        os.path.join(FIG_DIR, "task1_averaging_grid.png"),
        cols=3,
        figsize=(15, 8)
    )

    write_csv(os.path.join(TABLE_DIR, "task1_results.csv"), task1_rows)

    # --------------------------------------------------------
    # TASK 2
    # --------------------------------------------------------
    task2_rows = []
    task2_images = []
    task2_titles = []

    for variant in [4, 8]:
        response = laplacian_response(blurred, variant)
        response_display = normalize_to_uint8(np.abs(response))
        sharpened = laplacian_sharpen(blurred, variant)

        save_image(
            os.path.join(TASK2_DIR, f"laplacian_response_{variant}neighbor.png"),
            response_display
        )
        save_image(
            os.path.join(TASK2_DIR, f"laplacian_sharpened_{variant}neighbor.png"),
            sharpened
        )

        task2_images.extend([response_display, sharpened])
        task2_titles.extend([
            f"{variant}-neighbor response",
            f"{variant}-neighbor sharpened"
        ])

        task2_rows.append({
            "task": "Task 2",
            "configuration": f"Laplacian {variant}-neighbor",
            "noise_sigma": "",
            "kernel_size": 3,
            "parameter": variant,
            "psnr_db": round(psnr(gray, sharpened), 4),
            "sharpness_variance_laplacian": round(laplacian_variance(sharpened), 4),
            "mean_gradient_magnitude": round(mean_gradient_magnitude(sharpened), 4)
        })

    save_grid(
        task2_images,
        task2_titles,
        os.path.join(FIG_DIR, "task2_laplacian_grid.png"),
        cols=2,
        figsize=(12, 9)
    )

    write_csv(os.path.join(TABLE_DIR, "task2_results.csv"), task2_rows)

    # --------------------------------------------------------
    # TASK 3
    # --------------------------------------------------------
    task3_rows = []
    task3_images = []
    task3_titles = []

    k_values = [1.0, 1.5, 2.0, 3.0]
    sharpness_values = []

    for k in k_values:
        result = unsharp_highboost(noisy10, k=k, blur_size=5, blur_sigma=1.0)
        save_image(os.path.join(TASK3_DIR, f"unsharp_highboost_k{k}.png"), result)

        task3_images.append(result)
        task3_titles.append(f"k={k}")

        sharp = laplacian_variance(result)
        sharpness_values.append(sharp)

        task3_rows.append({
            "task": "Task 3",
            "configuration": f"High-boost k={k}",
            "noise_sigma": 10,
            "kernel_size": 5,
            "parameter": k,
            "psnr_db": round(psnr(gray, result), 4),
            "sharpness_variance_laplacian": round(sharp, 4),
            "mean_gradient_magnitude": round(mean_gradient_magnitude(result), 4)
        })

    save_grid(
        task3_images,
        task3_titles,
        os.path.join(FIG_DIR, "task3_highboost_grid.png"),
        cols=2,
        figsize=(12, 9)
    )

    plot_sharpness_curve(
        k_values,
        sharpness_values,
        os.path.join(FIG_DIR, "task3_sharpness_vs_k.png")
    )

    write_csv(os.path.join(TABLE_DIR, "task3_results.csv"), task3_rows)

    # --------------------------------------------------------
    # TASK 4: Combined table
    # --------------------------------------------------------
    all_rows = task1_rows + task2_rows + task3_rows
    write_csv(os.path.join(TABLE_DIR, "all_results.csv"), all_rows)

    plot_metric_comparison(
        all_rows,
        os.path.join(FIG_DIR, "psnr_comparison.png")
    )

    # --------------------------------------------------------
    # Reflection experiment: denoise -> sharpen vs sharpen -> denoise
    # --------------------------------------------------------
    denoise_then_sharpen = laplacian_sharpen(
        averaging_filter(noisy10, 5), variant=4
    )

    sharpen_then_denoise = averaging_filter(
        laplacian_sharpen(noisy10, 4), 5
    )

    order_rows = [
        {
            "configuration": "Denoise 5x5 -> Laplacian 4-neighbor",
            "psnr_db": round(psnr(gray, denoise_then_sharpen), 4),
            "sharpness_variance_laplacian": round(laplacian_variance(denoise_then_sharpen), 4)
        },
        {
            "configuration": "Laplacian 4-neighbor -> Denoise 5x5",
            "psnr_db": round(psnr(gray, sharpen_then_denoise), 4),
            "sharpness_variance_laplacian": round(laplacian_variance(sharpen_then_denoise), 4)
        }
    ]

    write_csv(os.path.join(TABLE_DIR, "reflection_order.csv"), order_rows)

    save_grid(
        [denoise_then_sharpen, sharpen_then_denoise],
        ["Denoise → Sharpen", "Sharpen → Denoise"],
        os.path.join(FIG_DIR, "reflection_order_comparison.png"),
        cols=2
    )

    # --------------------------------------------------------
    # High noise experiment
    # --------------------------------------------------------
    high_noise_rows = []
    for sigma in [25, 35, 50, 75, 100]:
        test = add_gaussian_noise(gray, sigma)
        for k in [1.0, 2.0, 3.0]:
            result = unsharp_highboost(test, k=k)
            high_noise_rows.append({
                "noise_sigma": sigma,
                "boost_k": k,
                "psnr_db": round(psnr(gray, result), 4),
                "sharpness_variance_laplacian": round(laplacian_variance(result), 4)
            })

    write_csv(os.path.join(TABLE_DIR, "high_noise_limit.csv"), high_noise_rows)

    # --------------------------------------------------------
    # Console summary
    # --------------------------------------------------------
    print("\nTask 1 results:")
    for row in task1_rows:
        print(
            f"{row['configuration']:<28} "
            f"PSNR={row['psnr_db']:>7.3f} dB  "
            f"Sharpness={row['sharpness_variance_laplacian']:>12.3f}"
        )

    print("\nTask 2 results:")
    for row in task2_rows:
        print(
            f"{row['configuration']:<28} "
            f"PSNR={row['psnr_db']:>7.3f} dB  "
            f"Sharpness={row['sharpness_variance_laplacian']:>12.3f}"
        )

    print("\nTask 3 results:")
    for row in task3_rows:
        print(
            f"{row['configuration']:<28} "
            f"PSNR={row['psnr_db']:>7.3f} dB  "
            f"Sharpness={row['sharpness_variance_laplacian']:>12.3f}"
        )

    best_psnr = max(all_rows, key=lambda x: x["psnr_db"])
    print("\nHighest PSNR configuration:")
    print(best_psnr["configuration"], best_psnr["psnr_db"], "dB")

    print("\nDone.")
    print("Outputs:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
