import cv2                       # cv - Open Source Computer Vision, allows us to control the camera
import os                        # os - operating system, allows to create files and folders on computer

from modules.Pixel_Detection import find_red_pixels, find_closest_pixel_to_centre, create_annotated_image, create_diagnostic_image

def initialise_camera(index=0):                     # This function turns on the camera when called
    webcam = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    """
    "Video.Capture" tells us which camera to use, by default webcam is "0", try 1 or -1 for external webcams
    "cv2.CAP_DSHOW" is the video capture backend for windows try, "cv2.CAP_ANY" for different OS
    """
    if not webcam.isOpened():                       # Checks if the webcam actually opened
        print("Error: Could not open camera")       # If webcam did not open tell user
        return None

    print("Camera ready!")              # If webcam did open tell user
    return webcam

def release_camera(webcam):             # This function deactivates the camera when called
    webcam.release()                    # The "release" function turns off the camera
    print("Camera released")            # Tells user camera us no longer in use

OUTPUT_FOLDER = "output"
def capture_image(webcam, image_number):              # This function captures the image when called, webcam must be initialized first
    ret, frame = webcam.read()
    """
    "ret" is a boolean that says whether the capture was successful or not
    "frame" is just a variable that temporarily store the image data
    "webcam.read()" is the function that takes the image
    """
    if not ret:                                       # if "ret" is false, no image was taken
        print("Error: Could not capture image")
        return None

    filename = f"image_{image_number:04d}.png"        # creates a file for the captured image
    filepath = os.path.join(OUTPUT_FOLDER, filename)  # specifies where to put image file
    cv2.imwrite(filepath, frame)                      # sends the image data stored in variable "frame" to file in output/raw

    print(f"Image saved: {filepath}")                 # notifies user that image was saved, and where it was saved
    return frame

def main():                                      # This is our main function where we will put all our commands
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "raw"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_FOLDER, "diagnostic"), exist_ok=True)
    """
    "exist_ok=True" input ensures this function only runs if the "output" file doesn't already exist
    "os.makedirs" creates output folder for images with the name "output" with "raw" folder inside
    """
    print("Pipe Scanner - Starting up...")
    print("Camera initialising...")

    """
    webcam = initialise_camera(index=0)          # Starts camera
    if webcam is None:
        return

    capture_image(webcam, 2)                    # Capture image
    release_camera(webcam)                      # Turns off camera
    """

    # load test image
    image_path = os.path.join(OUTPUT_FOLDER, "raw", "image_0001.png")
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Could not load image")
        return

    # find red pixels
    mask, red_pixels = find_red_pixels(image)
    print(f"Red pixels found: {len(red_pixels)}")

    # find closest pixel to centre
    closest_pixel, offset, centre_x = find_closest_pixel_to_centre(image, red_pixels)
    print(f"Closest pixel: {closest_pixel}")
    print(f"Centre line x: {centre_x}")
    print(f"Pixel offset: {offset}")

    # create and save diagnostic image
    diagnostic = create_diagnostic_image(image, mask, closest_pixel, offset, centre_x)
    cv2.imwrite(os.path.join(OUTPUT_FOLDER, "diagnostic", "image_0001_diagnostic.png"), diagnostic)
    print("Diagnostic image saved")

if __name__ == "__main__":  # This line just runs the code
    main()