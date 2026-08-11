# =========================================================
# ENTROPY
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
# PARAMETER SWEEP
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

        result = clahe_from_scratch(
            img,
            tile_rows=tile,
            tile_cols=tile,
            clip_limit=clip
        )

        value = entropy(result)

        results.append(
            (
                tile,
                clip,
                value
            )
        )

        filename = (
            f"tile_{tile}_clip_{clip}.jpg"
        )

        cv2.imwrite(
            os.path.join(
                output_folder,
                filename
            ),
            result
        )


# =========================================================
# PRINT RESULTS
# =========================================================

print("\n==============================================")
print("       CLAHE PARAMETER SWEEP RESULTS")
print("==============================================")

print(
    f"{'Tile Size':<15}"
    f"{'Clip Limit':<15}"
    f"{'Entropy':<15}"
)

for tile, clip, ent in results:

    print(
        f"{tile:<15}"
        f"{clip:<15}"
        f"{ent:<15.4f}"
    )
