import cv2
import numpy as np      # 'numpy' allows us to easy store and manipulate large arrays of numbers, we use this store image pixel data

# This function searches the image for the red pixels and returns a list of (x, y) coordinates for each red pixel found
def find_red_pixels(image):

    # convert image from BGR to HSV colour space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    """
    we convert to 'HSV' because it's easy to detect red dot using hue instead of 'BDR' values
    i.e. we can detect red pixels regardless of brightness
    """
    # define red colour range in HSV
    lower_red1 = np.array([0, 150, 150])            # values are (hue=0, saturation=155, brightness=150
    upper_red1 = np.array([10, 255, 255])           # values are (hue=10, saturation=255, brightness=255

    lower_red2 = np.array([170, 150, 150])
    upper_red2 = np.array([180, 255, 255])          # max values for each are (180, 255, 255)
    """
    Hue in HSV is defined using a scale of 0-180, 'Red' is defined from 0-10 and 170-180
    Therefore we need to define 'Red' for values with hues between 0-10 and 170-180
    """

    # create masks for both red ranges
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # combine both masks
    mask = cv2.bitwise_or(mask1, mask2)
    """
    The mask tells the computer where on the image red pixels were detected
    We create 2 masks, one for hue values 0-10 and another for hue values 170-180
    And then combine into a single mask 
    """

    # find coordinates of all red pixels
    red_pixels = np.column_stack(np.where(mask > 0))
    """
    'np.where()' finds the x and y coordinates of every pixel where 'red' is detected
    'np.column_stack' stores the x and y coordinates of each detected pixel
    """
    return mask, red_pixels     # returns the mask and the coordinates of the pixel

def find_closest_pixel_to_centre(image, red_pixels):
    """
    Finds the red pixel closest to the vertical center line of the image
    Returns the pixel coordinates and the offset distance in pixels
    """

    # get the image width and calculate the centre line x coordinate
    image_height, image_width = image.shape[:2]
    centre_x = image_width // 2
    """
    'image.shape' contains the (height, width and channels) of the image, we only need the 
    first 2 values so we use [:2]   
    """

    # start with a large number so any real distance will be smaller
    closest_pixel = None
    smallest_distance = float('inf')

    # loop through every red pixel and find the one closest to centre
    for pixel in red_pixels:
        y, x = pixel                         #  numpy returns [y, x] not [x, y]
        distance = abs(x - centre_x)         # horizontal distance to centre line
        if distance < smallest_distance:
            smallest_distance = distance
            closest_pixel = (x, y)

    # offset is positive if right of centre, negative if left of centre
    if closest_pixel is not None:
        offset = closest_pixel[0] - centre_x
    else:
        offset = None

    return closest_pixel, offset, centre_x

def create_annotated_image(image, closest_pixel, offset, centre_x):
    """
    Draws the centre line, highlights the detected pixel
    and shows the offset distance on the original image
    """
    # make a copy so we don't modify the original
    annotated = image.copy()

    image_height, image_width = image.shape[:2]

    # draw green centre line
    cv2.line(annotated, (centre_x, 0), (centre_x, image_height), (0, 255, 0), 2)

    if closest_pixel is not None:
        x, y = closest_pixel
        # draw red circle around detected pixel
        cv2.circle(annotated, (x, y), 20, (0, 0, 255), 2)
        # draw blue line showing offset distance
        cv2.line(annotated, (centre_x, y), (x, y), (255, 0, 0), 2)
        # draw offset text
        cv2.putText(annotated, f"Offset: {offset}px", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    return annotated


def create_diagnostic_image(image, mask, closest_pixel, offset, centre_x):
    """
    Creates a black background image with only red pixels visible,
    centre line and offset line drawn on
    """
    image_height, image_width = image.shape[:2]

    # create black image same size as original
    diagnostic = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # copy only red pixels from original image onto black background
    diagnostic[mask > 0] = image[mask > 0]

    # draw green centre line
    cv2.line(diagnostic, (centre_x, 0), (centre_x, image_height), (0, 255, 0), 2)

    if closest_pixel is not None:
        x, y = closest_pixel
        # draw blue line showing offset distance
        cv2.line(diagnostic, (centre_x, y), (x, y), (255, 0, 0), 2)
        # draw offset text
        cv2.putText(diagnostic, f"Offset: {offset}px", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    return diagnostic