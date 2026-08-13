#### import cv2
import os

# -------------------------------------------------
# IMAGE PATH
# -------------------------------------------------
image_path = r"C:\Users\yoges\Downloads\Cloudhoppers.jpg"

# Output folder
output_folder = r"C:\Users\yoges\Downloads\Image_Outputs"

# Create output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Load image
img = cv2.imread(image_path)

if img is None:
    print("Error: Image not found!")
    exit()

print("Image loaded successfully!")


# -------------------------------------------------
# MENU
# -------------------------------------------------

while True:

    print("\n========= IMAGE PROCESSING LAB =========")
    print("1. Display Image")
    print("2. Display Image Properties")
    print("3. Convert to Grayscale")
    print("4. Increase Brightness")
    print("5. Increase Contrast")
    print("6. Resize Image")
    print("7. Rotate Image")
    print("8. Flip Image")
    print("9. Crop Image")
    print("10. Negative Image")
    print("11. Save Image")
    print("12. Exit")

    choice = input("\nEnter your choice: ")


    # -------------------------------------------------
    # 1. DISPLAY IMAGE
    # -------------------------------------------------

    if choice == "1":

        cv2.imshow("Original Image", img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 2. IMAGE PROPERTIES
    # -------------------------------------------------

    elif choice == "2":

        height, width, channels = img.shape

        print("\n------ IMAGE PROPERTIES ------")
        print("Width       :", width)
        print("Height      :", height)
        print("Channels    :", channels)
        print("Data Type   :", img.dtype)
        print("Total Pixels:", width * height)


    # -------------------------------------------------
    # 3. GRAYSCALE
    # -------------------------------------------------

    elif choice == "3":

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Display
        cv2.imshow("Grayscale Image", gray)

        # Save
        filename = os.path.join(output_folder, "grayscale.jpg")
        cv2.imwrite(filename, gray)

        print("Grayscale image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 4. BRIGHTNESS
    # -------------------------------------------------

    elif choice == "4":

        brightness = 50

        bright = cv2.convertScaleAbs(
            img,
            alpha=1,
            beta=brightness
        )

        cv2.imshow("Bright Image", bright)

        # Save
        filename = os.path.join(output_folder, "brightness.jpg")
        cv2.imwrite(filename, bright)

        print("Bright image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 5. CONTRAST
    # -------------------------------------------------

    elif choice == "5":

        contrast = 1.5

        contrast_img = cv2.convertScaleAbs(
            img,
            alpha=contrast,
            beta=0
        )

        cv2.imshow("Contrast Image", contrast_img)

        # Save
        filename = os.path.join(output_folder, "contrast.jpg")
        cv2.imwrite(filename, contrast_img)

        print("Contrast image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 6. RESIZE
    # -------------------------------------------------

    elif choice == "6":

        width = int(input("Enter new width: "))
        height = int(input("Enter new height: "))

        resized = cv2.resize(img, (width, height))

        cv2.imshow("Resized Image", resized)

        # Save
        filename = os.path.join(output_folder, "resized.jpg")
        cv2.imwrite(filename, resized)

        print("Resized image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 7. ROTATE
    # -------------------------------------------------

    elif choice == "7":

        print("\n1. Rotate 90° Clockwise")
        print("2. Rotate 90° Counter-Clockwise")
        print("3. Rotate 180°")

        r = input("Enter rotation choice: ")

        if r == "1":

            rotated = cv2.rotate(
                img,
                cv2.ROTATE_90_CLOCKWISE
            )

        elif r == "2":

            rotated = cv2.rotate(
                img,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )

        elif r == "3":

            rotated = cv2.rotate(
                img,
                cv2.ROTATE_180
            )

        else:

            print("Invalid rotation choice!")
            continue

        cv2.imshow("Rotated Image", rotated)

        # Save
        filename = os.path.join(output_folder, "rotated.jpg")
        cv2.imwrite(filename, rotated)

        print("Rotated image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 8. FLIP
    # -------------------------------------------------

    elif choice == "8":

        print("\n1. Horizontal Flip")
        print("2. Vertical Flip")

        f = input("Enter flip choice: ")

        if f == "1":

            flipped = cv2.flip(img, 1)

        elif f == "2":

            flipped = cv2.flip(img, 0)

        else:

            print("Invalid flip choice!")
            continue

        cv2.imshow("Flipped Image", flipped)

        # Save
        filename = os.path.join(output_folder, "flipped.jpg")
        cv2.imwrite(filename, flipped)

        print("Flipped image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 9. CROP
    # -------------------------------------------------

    elif choice == "9":

        print("\nEnter crop coordinates")

        x1 = int(input("Enter x1: "))
        y1 = int(input("Enter y1: "))
        x2 = int(input("Enter x2: "))
        y2 = int(input("Enter y2: "))

        cropped = img[y1:y2, x1:x2]

        cv2.imshow("Cropped Image", cropped)

        # Save
        filename = os.path.join(output_folder, "cropped.jpg")
        cv2.imwrite(filename, cropped)

        print("Cropped image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 10. NEGATIVE
    # -------------------------------------------------

    elif choice == "10":

        negative = 255 - img

        cv2.imshow("Negative Image", negative)

        # Save
        filename = os.path.join(output_folder, "negative.jpg")
        cv2.imwrite(filename, negative)

        print("Negative image saved at:")
        print(filename)

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # -------------------------------------------------
    # 11. SAVE ORIGINAL IMAGE
    # -------------------------------------------------

    elif choice == "11":

        filename = input(
            "Enter filename (example: myimage.jpg): "
        )

        save_path = os.path.join(
            output_folder,
            filename
        )

        cv2.imwrite(save_path, img)

        print("\nImage saved successfully!")
        print("Location:", save_path)


    # -------------------------------------------------
    # 12. EXIT
    # -------------------------------------------------

    elif choice == "12":

        print("\nExiting program...")
        break


    else:

        print("\nInvalid choice! Please enter 1-12.")
