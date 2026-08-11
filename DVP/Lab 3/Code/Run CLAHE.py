# =========================================================
# APPLY CLAHE
# =========================================================

clahe_result = clahe_from_scratch(
    img,
    tile_rows=8,
    tile_cols=8,
    clip_limit=2.0
)


# Save
cv2.imwrite(
    os.path.join(
        output_folder,
        "clahe_from_scratch.jpg"
    ),
    clahe_result
)


# =========================================================
# DISPLAY
# =========================================================

plt.figure(figsize=(12, 5))

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

plt.title("Global Equalization")
plt.axis("off")


plt.subplot(1, 3, 3)

plt.imshow(
    clahe_result,
    cmap="gray"
)

plt.title("CLAHE")
plt.axis("off")


plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "CLAHE_comparison.png"
    ),
    dpi=300
)

plt.show()
