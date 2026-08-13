import cv2
import numpy as np
import os

# =========================================================
# IMAGE PATH
# =========================================================

image_path = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"

# Output folder
output_folder = r"C:\Users\yoges\Downloads\Lab2_Outputs"

# Create output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)


# =========================================================
# LOAD IMAGE
# =========================================================

img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Error: Image not found!")
    exit()

print("Image loaded successfully!")
print("Image path:", image_path)


# =========================================================
# MENU
# =========================================================

while True:

    print("\n==============================================")
    print("              DVP LAB - LAB 2")
    print("        IMAGE ENHANCEMENT")
    print("       TRANSFORMATION FUNCTIONS")
    print("==============================================")

    print("\n1. Negative - Without Library")
    print("2. Negative - With Library")

    print("3. Power Law / Gamma - Without Library")
    print("4. Power Law / Gamma - With Library")

    print("5. Log Transformation - Without Library")
    print("6. Log Transformation - With Library")

    print("7. Exit")

    choice = input("\nEnter your choice: ")


    # =====================================================
    # 1. NEGATIVE WITHOUT LIBRARY
    # =====================================================

    if choice == "1":

        print("\n--- Negative Transformation Without Library ---")

        # L = 256 for 8-bit image
        L = 256

        # Create an empty image
        negative = np.zeros_like(img)

        # Formula:
        # S = L - 1 - r

        for i in range(img.shape[0]):

            for j in range(img.shape[1]):

                # Convert uint8 to normal integer
                r = int(img[i, j])

                # Negative transformation
                s = L - 1 - r

                # Store output
                negative[i, j] = s

        # Display
        cv2.imshow(
            "Negative - Without Library",
            negative
        )

        # Save
        path = os.path.join(
            output_folder,
            "negative_without_library.jpg"
        )

        cv2.imwrite(path, negative)

        print("Image saved successfully!")
        print("Location:", path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # =====================================================
    # 2. NEGATIVE WITH LIBRARY
    # =====================================================

    elif choice == "2":

        print("\n--- Negative Transformation With Library ---")

        # OpenCV library function
        negative = cv2.bitwise_not(img)

        # Display
        cv2.imshow(
            "Negative - With Library",
            negative
        )

        # Save
        path = os.path.join(
            output_folder,
            "negative_with_library.jpg"
        )

        cv2.imwrite(path, negative)

        print("Image saved successfully!")
        print("Location:", path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # =====================================================
    # 3. POWER LAW / GAMMA WITHOUT LIBRARY
    # =====================================================

    elif choice == "3":

        print("\n--- Power Law / Gamma Without Library ---")

        gamma = float(
            input("Enter gamma value (example 0.5 or 2): ")
        )

        # Constant
        c = 1

        # Create empty image
        gamma_img = np.zeros_like(img)

        # Formula:
        # S = c(r^gamma)

        for i in range(img.shape[0]):

            for j in range(img.shape[1]):

                # Convert pixel from 0-255 to 0-1
                r = int(img[i, j]) / 255.0

                # Apply power law
                s = c * (r ** gamma)

                # Convert back to 0-255
                s = int(s * 255)

                # Store output
                gamma_img[i, j] = s

        # Display
        cv2.imshow(
            "Gamma - Without Library",
            gamma_img
        )

        # Save
        path = os.path.join(
            output_folder,
            "gamma_without_library.jpg"
        )

        cv2.imwrite(path, gamma_img)

        print("Image saved successfully!")
        print("Location:", path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # =====================================================
    # 4. POWER LAW / GAMMA WITH LIBRARY
    # =====================================================

    elif choice == "4":

        print("\n--- Power Law / Gamma With Library ---")

        gamma = float(
            input("Enter gamma value (example 0.5 or 2): ")
        )

        # Normalize image
        normalized = img.astype(np.float32) / 255.0

        # Apply power law using NumPy
        gamma_img = np.power(
            normalized,
            gamma
        )

        # Convert back to 0-255
        gamma_img = np.uint8(
            gamma_img * 255
        )

        # Display
        cv2.imshow(
            "Gamma - With Library",
            gamma_img
        )

        # Save
        path = os.path.join(
            output_folder,
            "gamma_with_library.jpg"
        )

        cv2.imwrite(path, gamma_img)

        print("Image saved successfully!")
        print("Location:", path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # =====================================================
    # 5. LOG TRANSFORMATION WITHOUT LIBRARY
    # =====================================================

    elif choice == "5":

        print("\n--- Log Transformation Without Library ---")

        # Constant:
        # c = 255 / log(1 + 255)
        c = 255 / np.log(256)

        # Create empty image
        log_img = np.zeros_like(img)

        # Formula:
        # S = c log(1 + r)

        for i in range(img.shape[0]):

            for j in range(img.shape[1]):

                # IMPORTANT:
                # Convert uint8 pixel to normal integer
                r = int(img[i, j])

                # Apply log transformation
                s = c * np.log(1 + r)

                # Convert result to integer
                s = int(s)

                # Store output
                log_img[i, j] = s

        # Display
        cv2.imshow(
            "Log - Without Library",
            log_img
        )

        # Save
        path = os.path.join(
            output_folder,
            "log_without_library.jpg"
        )

        cv2.imwrite(path, log_img)

        print("Image saved successfully!")
        print("Location:", path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # =====================================================
    # 6. LOG TRANSFORMATION WITH LIBRARY
    # =====================================================

    elif choice == "6":

        print("\n--- Log Transformation With Library ---")

        # Constant
        c = 255 / np.log(256)

        # Convert image to float
        img_float = img.astype(np.float32)

        # Apply log transformation
        log_img = c * np.log(
            1 + img_float
        )

        # Convert to uint8
        log_img = np.uint8(log_img)

        # Display
        cv2.imshow(
            "Log - With Library",
            log_img
        )

        # Save
        path = os.path.join(
            output_folder,
            "log_with_library.jpg"
        )

        cv2.imwrite(path, log_img)

        print("Image saved successfully!")
        print("Location:", path)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # =====================================================
    # 7. EXIT
    # =====================================================

    elif choice == "7":

        print("\n==============================================")
        print("Program terminated successfully.")
        print("==============================================")

        break


    # =====================================================
    # INVALID CHOICE
    # =====================================================

    else:

        print("\nInvalid choice!")
        print("Please enter a number from 1 to 7.")
