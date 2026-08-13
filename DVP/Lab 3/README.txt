## Results

The spatial filtering experiments were successfully performed on the degraded AGV camera image. The results demonstrate the effect of averaging filters, Laplacian sharpening, and unsharp/high-boost filtering on noise suppression and edge enhancement.

### 1. Noise Suppression Using Averaging Filters

The noisy images generated with **σ = 10** and **σ = 25** were processed using averaging filters of sizes **3×3, 5×5, and 9×9**.

The **3×3 filter** provided moderate noise reduction while preserving most object boundaries and fine image details. The **5×5 filter** produced stronger noise suppression but introduced some loss of fine texture. The **9×9 filter** removed a large amount of noise; however, it also caused noticeable blurring of obstacle boundaries and small structures.

The results show the expected trade-off: increasing the kernel size improves noise suppression but reduces spatial detail. This effect was more noticeable for the image with **σ = 25**, where stronger smoothing was required.

### 2. Laplacian Sharpening

Laplacian sharpening was applied to the motion-blurred image using both **4-neighbor** and **8-neighbor** Laplacian kernels.

The **4-neighbor Laplacian** primarily responds to intensity changes in the horizontal and vertical directions, while the **8-neighbor Laplacian** also considers diagonal intensity changes. Consequently, the 8-neighbor version produced stronger responses around diagonal and irregular object boundaries.

The Laplacian response maps clearly highlighted obstacle boundaries and other high-frequency structures affected by motion blur. The comparison between the two variants was evaluated using both visual inspection and the calculated sharpness metric.

### 3. Unsharp Masking and High-Boost Filtering

Unsharp masking was performed with **k = 1**, followed by high-boost filtering with **k = 1.5, 2, and 3**.

Increasing the value of **k** increased the strength of edge enhancement. At lower values, the processed image showed improved boundary definition while retaining relatively natural appearance. As **k** increased further, fine edges became more prominent, but noise and small unwanted intensity variations were also amplified.

Therefore, the highest value of **k** was not automatically considered the best configuration. The final value was selected by comparing the improvement in the sharpness metric with the corresponding PSNR and observing whether additional sharpening was actually beneficial.

### 4. Quantitative Evaluation

Each processed image was compared with the original clean image using two objective measures:

* **PSNR:** Measures the similarity between the processed image and the clean ground truth. Higher PSNR generally indicates lower pixel-level reconstruction error.
* **Sharpness:** Measured using the **variance of the Laplacian**, where a higher value indicates stronger high-frequency content and sharper edges.

The quantitative results confirmed that smoothing filters generally improved PSNR by reducing noise, while excessive smoothing reduced sharpness. Conversely, sharpening increased the sharpness metric but could reduce PSNR when noise was also amplified.

Thus, the results demonstrate that **PSNR and sharpness must be considered together** rather than selecting a filter based on a single metric.

### 5. Final Pipeline Result

Based on the experimental results, the recommended AGV preprocessing pipeline is:

**Degraded Input → Averaging Filter → Laplacian/Unsharp Sharpening → Enhanced Image**

A moderate averaging filter was preferred because it provided sufficient noise suppression without excessively blurring navigation-relevant boundaries. This was followed by controlled sharpening to restore obstacle edges and improve boundary visibility.

The final configuration was selected from the tested parameters using the **PSNR–sharpness trade-off**, rather than simply choosing the configuration with the highest numerical sharpness.

### Overall Result

The experiment demonstrates that spatial filtering can effectively improve a degraded onboard camera image, but **no single filter is optimal for all degradation conditions**. Large smoothing kernels provide better noise suppression but can destroy important edges, while aggressive sharpening can enhance both useful boundaries and unwanted noise. Therefore, a balanced combination of **moderate denoising followed by controlled sharpening** provides the most suitable preprocessing strategy for an AGV perception pipeline.
