import cv2
import os
import time
import numpy as np

from modules.Pixel_Detection import *
from modules.Serial_Com import *
from modules.Cam_Control import *

PORT = "COM5"
BAUD = 9600


def RunTest(arduino):
    print("Starting up...")
    print("Camera initialising...")

    webcam = initialise_camera(index=0)
    if webcam is None:
        return None, None, None, None, None

    laser_on(arduino)
    time.sleep(2)
    capture_image(webcam, 1)
    release_camera(webcam)
    time.sleep(3)
    laser_off(arduino)

    # load test image
    image_path = os.path.join(OUTPUT_FOLDER, "raw", "image_0001.png")
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not load image")
        return None, None, None, None, None

    # find red pixels
    mask, red_pixels = find_red_pixels(image)
    print(f"Red pixels found: {len(red_pixels)}")

    # find closest pixel to centre
    closest_pixel, offset, centre_x = find_closest_pixel_to_centre(image, red_pixels)
    print(f"Closest pixel: {closest_pixel}")
    print(f"Centre line x: {centre_x}")
    print(f"Pixel offset: {offset}")

    return offset, image, mask, closest_pixel, centre_x


def main():
    git
    push
    origin
    main - -force
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "raw"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "diagnostic"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "calibration"), exist_ok=True)

    # connect once at the start of the session
    arduino = connect(PORT, BAUD)
    if arduino is None:
        print("Error: Could not connect to Arduino, exiting...")
        return

    common_ratio = None
    mm_per_pixel = None

    UserSelection = None
    while UserSelection != 3:
        print("\nSelect Option: ")
        print("(1) Calibrate")
        print("(2) Run Test")
        print("(3) Exit")
        UserSelection = int(input())

        if UserSelection == 1:
            offset, image, mask, closest_pixel, centre_x = RunTest(arduino)

            if offset is None:
                print("Error: Test failed, calibration aborted")
                continue

            # create and save calibration image
            calibration = create_calibration_image(image, mask, closest_pixel, offset, centre_x)
            cv2.imwrite(os.path.join(OUTPUT_FOLDER, "calibration", "image_0001_calibration.png"), calibration)
            print("Calibration image saved")

            # get calibration info from user
            print("Enter Measured Values")
            vertical_distance = float(input("Vertical Distance (mm): "))
            horizontal_distance = float(input("Horizontal Distance (mm): "))

            common_ratio = horizontal_distance / vertical_distance
            mm_per_pixel = vertical_distance / offset
            print("Calibration complete!")

        if UserSelection == 2:
            if common_ratio is None or mm_per_pixel is None:
                print("Error: Please run calibration first (Option 1)")
            else:
                offset, image, mask, closest_pixel, centre_x = RunTest(arduino)

                if offset is None:
                    print("Error: Test failed")
                    continue

                # create and save diagnostic image
                diagnostic = create_diagnostic_image(image, mask, closest_pixel, offset, centre_x)
                cv2.imwrite(os.path.join(OUTPUT_FOLDER, "diagnostic", "image_0001_diagnostic.png"), diagnostic)
                print("Diagnostic image saved")

                # find horizontal distance in mm
                horizontal_distance_pixel = offset * common_ratio
                result = horizontal_distance_pixel * mm_per_pixel
                print(f"Horizontal distance: {result:.2f} mm")

                step_motor(arduino)

        if UserSelection == 3:
            print("Exiting...")

    # disconnect once at the end of the session
    disconnect(arduino)


if __name__ == "__main__":
    main()