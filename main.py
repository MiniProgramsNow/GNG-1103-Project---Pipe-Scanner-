import cv2                       # cv - Open Source Computer Vision, allows us to control the camera
import os                        # os - operating system, allows to create files and folders on computer

def initialise_camera(index=0):                     # This function turns on the camera when called
    webcam = cv2.VideoCapture(index, cv2.CAP_DSHOW) # Video.Capture tells us which camera to use, by default webcam is "0", try 1 or -1 for external webcams
                                                    # "cv2.CAP_DSHOW" is the video capture backend for windows try, "cv2.CAP_ANY" for different OS

    if not webcam.isOpened():                       # Checks if the webcam actually opened
        print("Error: Could not open camera")       # If webcam did not open tell user
        return None

    print("Camera ready!")              # If webcam did open tell user
    return webcam

def release_camera(webcam):             # This function deactivates the camera when called
    webcam.release()                    # The "release" function turns off the camera
    print("Camera released")            # Tells user camera us no longer in use

OUTPUT_FOLDER = "output/raw"                          # variable we use to create 2 files "output" and "raw" with the "raw" file inside
def capture_image(webcam, image_number):              # This function captures the image when called, webcam must be initialized first
    ret, frame = webcam.read()                        # "ret" is a boolean that says whether the capture was successful or not
                                                      # "frame" is just a variable that temporarily store the image data
                                                      # "webcam.read()" is the function that takes the image

    if not ret:                                       # if "ret" is false, no image was taken
        print("Error: Could not capture image")
        return None

    filename = f"image_{image_number:04d}.png"        # creates a file for the captured image
    filepath = os.path.join(OUTPUT_FOLDER, filename)  # specifies where to put image file
    cv2.imwrite(filepath, frame)                      # sends the image data stored in variable "frame" to file in output/raw

    print(f"Image saved: {filepath}")                 # notifies user that image was saved, and where it was saved
    return frame

def main():                                      # This is our main function where we will put all our commands
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)    # The "exist_ok=True" input ensures this function only runs if the file doesn't already exist
                                                 # os.makedirs creates output folder for images with the name "output" with "raw" folder inside
    print("Pipe Scanner - Starting up...")
    print("Camera initialising...")

    webcam = initialise_camera(index=0)          # Starts camera
    if webcam is None:
        return

    capture_image(webcam, 1)        # Capture image

    release_camera(webcam)                      # Turns off camera

if __name__ == "__main__":  # This line just runs the code
    main()