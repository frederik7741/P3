import numpy as np
import pyzed.sl as sl
import math
import cv2
import main

"""
Check list:
**train on a bunch of pictures (different poses)**
select key points manually (probably down grade to BODY_FORMAT_18 or something custom)
    this is a real world pixel coordinate
use a kernel to assure that the pixel doesn't float away (if its noisy or affected by lighting)
    this is a virtual world pixel coordinate
    if any point inside the kernel area is too far away -> ignore it for this frames calculation
access the depth data from each of the specific keypoints

i dunno, maybe at some point the program just learns what limbs are and can do it all by itself
"""


def on_mouse_click(event, x, y, flags, param):
    clicked_pixel = [x, y]

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse clicked at:{clicked_pixel}. Depth:{get_pixel_depth(clicked_pixel)}")

    elif event == cv2.EVENT_RBUTTONDOWN:
        get_neighbour_pixel_depths(clicked_pixel)


def get_pixel_depth(pixel):
    distance = main.depth.get_value(pixel)
    print(f"Depth at pixel ({pixel}): {distance} meters")
    return distance


def get_neighbour_pixel_depths(pixel):
    pixel_list = []
    avg_depth = 0

    for i in range(-3, 3):
        for j in range(-3, 3):
            temp_pixel = pixel[0] + i, pixel[1] + j
            temp_pixel_depth = get_pixel_depth(temp_pixel)
            dead_pixel = False

            for pixel_depth in pixel_list:
                if temp_pixel_depth - 10 > pixel_depth > temp_pixel_depth + 10:  # 10 millimeters
                    dead_pixel = True
                    break

            if dead_pixel is False:
                pixel_list.append(temp_pixel_depth)

    for depth in pixel_list:
        avg_depth += depth / len(pixel_list)  # this actually makes sense somehow

    print(avg_depth)
    return avg_depth


image_path = "C:/Users/Mikkel Rusbak/Pictures/Saved Pictures/alien and fwiend.png"
# depth_image = zed.retrieve_image(main.depth_image, sl.VIEW.DEPTH)

# Read the image using cv2
image = cv2.imread(image_path)
# image = cv2.imread(depth_image)

# Create a window and display the image
cv2.namedWindow("ZED Camera Image Viewer")
cv2.imshow("ZED Camera Image Viewer", image)

# Set the mouse callback function
cv2.setMouseCallback("ZED Camera Image Viewer", on_mouse_click)

# Wait for a key event and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()