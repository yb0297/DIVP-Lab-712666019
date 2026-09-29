import cv2
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. DEFINE THE KERNELS
# ============================================================

# (a) 2nd derivative / Laplacian
K1 = np.array([
    [1,  1,  1],
    [1, -8,  1],
    [1,  1,  1]
], dtype=np.float32)

# (b) 1st derivative
K2 = np.array([
    [-1, -1, -1],
    [ 2,  2,  2],
    [-1, -1, -1]
], dtype=np.float32)

# (c) 2nd derivative
K3 = np.array([
    [-1,  2, -1],
    [-1,  2, -1],
    [-1,  2, -1]
], dtype=np.float32)

# (d) 2nd derivative / diagonal
K4 = np.array([
    [ 2, -1, -1],
    [-1,  2, -1],
    [-1, -1,  2]
], dtype=np.float32)


# ============================================================
# 2. CREATE TEST IMAGES
# ============================================================

# V1: 1-pixel-wide diagonal line
V1 = np.zeros((100, 100), dtype=np.uint8)
cv2.line(V1, (20, 80), (80, 20), 255, 1)

# V2: 3-pixel-wide vertical line
V2 = np.zeros((100, 100), dtype=np.uint8)
cv2.line(V2, (50, 20), (50, 80), 255, 3)


# ============================================================
# 3. APPLY KERNELS
# ============================================================

def apply_kernels(image):

    # Use CV_32F so negative derivative values are preserved
    image_float = image.astype(np.float32)

    R1 = cv2.filter2D(image_float, cv2.CV_32F, K1)
    R2 = cv2.filter2D(image_float, cv2.CV_32F, K2)
    R3 = cv2.filter2D(image_float, cv2.CV_32F, K3)
    R4 = cv2.filter2D(image_float, cv2.CV_32F, K4)

    return R1, R2, R3, R4


R1_V1, R2_V1, R3_V1, R4_V1 = apply_kernels(V1)
R1_V2, R2_V2, R3_V2, R4_V2 = apply_kernels(V2)


# ============================================================
# 4. DISPLAY RESULTS
# ============================================================

fig, ax = plt.subplots(2, 5, figsize=(15, 6))

# ---------------- V1 ----------------

ax[0, 0].imshow(V1, cmap="gray")
ax[0, 0].set_title("V1: 1-pixel diagonal")

ax[0, 1].imshow(R1_V1, cmap="gray")
ax[0, 1].set_title("Kernel 1")

ax[0, 2].imshow(R2_V1, cmap="gray")
ax[0, 2].set_title("Kernel 2")

ax[0, 3].imshow(R3_V1, cmap="gray")
ax[0, 3].set_title("Kernel 3")

ax[0, 4].imshow(R4_V1, cmap="gray")
ax[0, 4].set_title("Kernel 4")


# ---------------- V2 ----------------

ax[1, 0].imshow(V2, cmap="gray")
ax[1, 0].set_title("V2: 3-pixel vertical")

ax[1, 1].imshow(R1_V2, cmap="gray")
ax[1, 1].set_title("Kernel 1")

ax[1, 2].imshow(R2_V2, cmap="gray")
ax[1, 2].set_title("Kernel 2")

ax[1, 3].imshow(R3_V2, cmap="gray")
ax[1, 3].set_title("Kernel 3")

ax[1, 4].imshow(R4_V2, cmap="gray")
ax[1, 4].set_title("Kernel 4")


for a in ax.ravel():
    a.axis("off")

plt.tight_layout()
plt.show()


# ============================================================
# 5. GIVEN PIXEL ARRAY
# ============================================================

# IMPORTANT:
# Your original array has:
# Row 1 -> 8 values
# Row 2 -> 9 values
# Row 3 -> 7 values
#
# Therefore it is NOT a valid rectangular NumPy array.
#
# Correct the following array according to your assignment.

Ip = np.array([
    [5, 5, 4, 3, 2, 1, 0, 0],
    [0, 6, 0, 0, 0, -1, 3, 1],
    [0, 0, 0, 0, 7, 7, 5, 0]   # <-- CHECK THIS LAST VALUE
], dtype=np.float32)


print("\nInput Array:")
print(Ip)


# ============================================================
# 6. FIRST DERIVATIVE
# ============================================================

# Derivative in X direction
Dx = np.diff(Ip, axis=1)

# Derivative in Y direction
Dy = np.diff(Ip, axis=0)

print("\nFirst Derivative Dx:")
print(Dx)

print("\nFirst Derivative Dy:")
print(Dy)


# ============================================================
# 7. SECOND DERIVATIVE
# ============================================================

# Second derivative in X direction
Dxx = np.diff(Ip, n=2, axis=1)

# Second derivative in Y direction
Dyy = np.diff(Ip, n=2, axis=0)

print("\nSecond Derivative Dxx:")
print(Dxx)

print("\nSecond Derivative Dyy:")
print(Dyy)
