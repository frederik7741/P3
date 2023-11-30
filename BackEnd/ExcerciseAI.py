import cv2
import sys
import pyzed.sl as sl
import ogl_viewer.viewer as gl
import cv_viewer.tracking_viewer as cv_viewer
import numpy as np
import argparse
import math

# Function to calculate the angle between three points
def calculate_angle(p1, p2, p3):
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle

def main():
    zed = sl.Camera()  # Create a Camera object

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.coordinate_units = sl.UNIT.METER  # Set coordinate units
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Get camera information for initializing the viewer
    camera_info = zed.get_camera_information()

    # Setup body tracking parameters
    body_param = sl.BodyTrackingParameters()
    body_param.enable_tracking = True
    body_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
    body_param.body_format = sl.BODY_FORMAT.BODY_18  # Choose the BODY_FORMAT you wish to use
    zed.enable_body_tracking(body_param)

    # Initialize OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(camera_info.camera_configuration.calibration_parameters.left_cam, body_param.enable_tracking,body_param.body_format)

    # Initialize other variables
    bodies = sl.Bodies()
    image = sl.Mat()
    key_wait = 10

    # Main loop
    while viewer.is_available():
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT, sl.MEM.CPU, display_resolution)
            zed.retrieve_bodies(bodies, body_param)
            viewer.update_view(image, bodies)

            for body in bodies.body_list:
                keypoints = body.keypoints

                # Assuming keypoints 2, 3, and 4 are shoulder, elbow, and wrist respectively
                shoulder = keypoints[2].get_position()
                elbow = keypoints[3].get_position()
                wrist = keypoints[4].get_position()

                # Calculate the angle
                angle = calculate_angle(shoulder, elbow, wrist)
                print("Angle between shoulder, elbow, and wrist: ", angle)

    # Cleanup
    viewer.exit()
    zed.disable_body_tracking()
    zed.disable_positional_tracking()
    zed.close()

if __name__ == '__main__':
    main()
