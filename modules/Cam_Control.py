import cv2
import os

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
def capture_image(webcam, image_number):  # This function captures the image when called, webcam must be initialized first
    ret, frame = webcam.read()
    """
    "ret" is a boolean that says whether the capture was successful or not
    "frame" is just a variable that temporarily store the image data
    "webcam.read()" is the function that takes the image
    """
    if not ret:  # if "ret" is false, no image was taken
        print("Error: Could not capture image")
        return None

    filename = f"image_{image_number:04d}.png"  # creates a file for the captured image
    filepath = os.path.join(OUTPUT_FOLDER, "raw", filename)  # specifies where to put image file
    cv2.imwrite(filepath, frame)  # sends the image data stored in variable "frame" to file in output/raw

    print(f"Image saved: {filepath}")  # notifies user that image was saved, and where it was saved
    return frame