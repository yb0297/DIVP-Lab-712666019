# =========================================================
# ANALYTICAL TARGET HISTOGRAM
# =========================================================

def create_moody_target():

    intensity = np.arange(256)

    # Dark/shadow-heavy Gaussian distribution
    center = 70
    sigma = 35

    target = np.exp(
        -((intensity - center) ** 2)
        / (2 * sigma ** 2)
    )

    # Normalize
    target = target / np.sum(target)

    return target


# =========================================================
# MATCH TO ANALYTICAL TARGET
# =========================================================

def histogram_matching_target(source, target_pdf):

    source_hist = np.bincount(
        source.ravel(),
        minlength=256
    )

    source_pdf = source_hist / source.size

    source_cdf = np.cumsum(source_pdf)

    target_cdf = np.cumsum(target_pdf)

    mapping = np.zeros(256, dtype=np.uint8)

    for r in range(256):

        difference = np.abs(
            target_cdf - source_cdf[r]
        )

        mapping[r] = np.argmin(difference)

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
plt.imshow(moody_image, cmap="gray")
plt.title("Moody Target Result")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.plot(target_pdf)
plt.title("Analytical Target Histogram")
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
