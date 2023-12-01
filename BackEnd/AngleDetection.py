# for at regne vinklerne mellem led, definerer vi leddene som en 3D vektor og finder vinklen derimellem

import numpy as np
import math
# import main

def points_to_bones(point_1, point_2):
    print("point_1:", point_1)
    print("point_2:", point_2)

    # Check if point_1 and point_2 are tuples
    if not (isinstance(point_1, tuple) and isinstance(point_2, tuple)):
        raise ValueError("Invalid input points")

    # Extract (x, y) coordinates from the tuples
    if isinstance(point_1[1], tuple):
        x1, y1 = point_1[1]
    elif isinstance(point_1[1], (int, float)):
        x1, y1 = point_1[1], point_1[1]
    else:
        raise ValueError("Invalid input points")

    if isinstance(point_2[1], tuple):
        x2, y2 = point_2[1]
    elif isinstance(point_2[1], (int, float)):
        x2, y2 = point_2[1], point_2[1]
    else:
        raise ValueError("Invalid input points")

    # Calculate bone vector
    bone_vector = [x2 - x1, y2 - y1]

    return bone_vector










def find_angle(bone_1, bone_2):
    if np.all(bone_1 == 0) or np.all(bone_2 == 0):
        return 0.0  # You can modify this value based on how you want to handle zero vectors

    upper_dot_product = np.dot(bone_1, bone_2)
    lower_dot_product = np.linalg.norm(bone_1) * np.linalg.norm(bone_2)

    if lower_dot_product == 0:
        return 0.0  # Handle division by zero appropriately

    cosine_angle = upper_dot_product / lower_dot_product
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))  # Ensure the value is within the valid range for arccos

    return np.degrees(angle)


#detected_body = bodies.get_first_body_2d_image()

# # Structures for detected bodies
# # body_data = sl.BodyTrackingData()  # Create an instance of the body tracking data (do this elsewhere in another script)
# bodies = sl.Bodies()  # Structure containing all the detected bodies
# body_part = sl.BODY_38_PARTS  # Not sure about this one
#
# # Set initialization parameters
# body_detection_parameters = sl.BodyTrackingParameters()
# body_detection_parameters.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE
# body_detection_parameters.enable_tracking = True  # Track people across images flow
# body_detection_parameters.enable_body_fitting = True  # Smooth skeleton move
# body_detection_parameters.body_format = sl.BODY_FORMAT.BODY_38
#
# # Set runtime parameters
# runtime_body_detection_parameters = sl.BodyTrackingRuntimeParameters()
# runtime_body_detection_parameters.detection_confidence_threshold = 40
#
# # Camera setup
# zed = sl.Camera()
# if zed.grab(runtime_body_detection_parameters) == sl.ERROR_CODE.SUCCESS:
#     zed.retrieve_image(main.depth_image, sl.VIEW.LEFT)  # Get image from somewhere else
#     # zed.retrieve_measure(body_data, sl.BODY_FORMAT.BODY_38)
#     zed.retrieve_bodies(bodies, sl.BODY_FORMAT.BODY_38)
#
# # Set positional tracking parameters
# body_detection_parameters.enable_tracking = True
# if body_detection_parameters.enable_tracking:
#     # Set positional tracking parameters
#     positional_tracking_parameters = sl.PositionalTrackingParameters()
#     # Enable positional tracking
#     zed.enable_positional_tracking(positional_tracking_parameters)
#
# # Set body tracking parameters
# body_tracking_parameters = sl.BodyTrackingParameters()
# body_tracking_parameters.enable_body_fitting = True  # Enable body tracking
# zed_error = zed.enable_body_tracking(body_detection_parameters)
# if zed_error != sl.ERROR_CODE.SUCCESS:
#     print("enable_body_tracking", zed_error, "\nExit program.")
#     zed.close()
#     exit(-1)