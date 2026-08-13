Results
1. Noise Suppression Using Averaging Filters

Averaging filters were applied to the degraded AGV camera images with Gaussian noise levels of σ = 10 and σ = 25 using 3×3, 5×5, and 9×9 kernels.

3×3: Provided moderate noise reduction while preserving most object boundaries and fine details.
5×5: Produced stronger noise suppression with some loss of fine texture and edge sharpness.
9×9: Provided the strongest smoothing, but significantly blurred obstacle boundaries and small structures.

The experiment demonstrates the trade-off between noise suppression and edge preservation. Larger kernels remove more noise but also remove more useful spatial information.

2. Laplacian Sharpening

Laplacian sharpening was applied to the motion-blurred image using both 4-neighbor and 8-neighbor Laplacian kernels.

The 4-neighbor kernel responds mainly to horizontal and vertical intensity changes, whereas the 8-neighbor kernel also responds to diagonal changes. Therefore, the 8-neighbor version generally produces stronger responses around diagonal and irregular object boundaries.

The Laplacian response images clearly emphasize high-frequency regions such as obstacle boundaries, edges, and fine structures affected by motion blur.

3. Unsharp Masking and High-Boost Filtering

Unsharp masking and high-boost filtering were tested using:

k = 1 — Unsharp masking
k = 1.5
k = 2
k = 3

As k increased, edge strength increased and boundaries became more prominent. However, excessive sharpening also amplified noise and unwanted high-frequency variations.

Therefore, the largest value of k was not automatically considered the best. The suitable value was selected by considering both PSNR and sharpness and by observing whether additional sharpening provided useful edge enhancement or mainly amplified noise.

4. Quantitative Evaluation

Every processed image was compared with the original clean image using two metrics.

PSNR

Peak Signal-to-Noise Ratio (PSNR) measures the pixel-level similarity between the processed image and the clean ground truth.

Higher PSNR generally indicates lower reconstruction error.

Sharpness

Image sharpness was measured using the variance of the Laplacian.

Higher variance indicates stronger high-frequency content and therefore stronger edges.

The results showed that averaging filters generally improved PSNR by reducing noise, but excessive smoothing decreased the sharpness of important boundaries.

Sharpening increased the sharpness metric, but aggressive sharpening could decrease PSNR because noise was enhanced along with useful edges.

Therefore, PSNR and sharpness must be evaluated together rather than selecting a configuration using only one metric.

5. Final Pipeline Recommendation

Based on the experimental observations and quantitative evaluation, the recommended preprocessing pipeline is:

Degraded AGV Camera Frame
          ↓
   Noise Reduction
          ↓
   Controlled Sharpening
          ↓
 Enhanced Camera Frame
          ↓
Obstacle Detection / Terrain Classification

A moderate averaging filter is preferred for the denoising stage because it provides a good balance between noise suppression and edge preservation.

This is followed by controlled sharpening using Laplacian or unsharp/high-boost filtering to restore the visibility of obstacle boundaries.

The final parameters should be selected from the configuration that provides a suitable balance between high PSNR, sufficient sharpness, and preservation of navigation-relevant edges.

Overall Result

The experiment demonstrates that spatial filtering can significantly improve degraded AGV camera images. However, no single filter or parameter value is optimal for every degradation condition.

Large averaging kernels provide stronger noise suppression but can destroy important edges. Conversely, aggressive sharpening can improve edge strength while simultaneously amplifying noise.

Therefore, the experimental results support a two-stage preprocessing approach:

Moderate denoising → Controlled sharpening

This approach provides a practical balance between noise reduction, edge preservation, and boundary enhancement, making it suitable as a preprocessing stage for subsequent AGV tasks such as obstacle boundary detection and terrain classification.
