# for at regne vinklerne mellem led, definerer vi leddene som en 3D vektor og finder vinklen derimellem

import numpy as np
import math
# import main

def points_to_bones(point_1, point_2):
    bone_vector = [point_2[0] - point_1[0], point_2[1] - point_1[1]]  # , point_2[2] - point_1[2]
    #bone_origin = point_1
    #bone = bone_length, bone_origin
    return bone_vector


def find_angle(bone_1, bone_2):
    upper_dot_product = bone_1[0] * bone_2[0] + bone_1[1] * bone_2[1]  # + bone_1[2] * bone_2[2]
    # print(f"Upper product: {upper_dot_product}")

    lower_dot_product = (math.sqrt(bone_1[0] ** 2 + bone_1[1] ** 2) *  #  + bone_1[2] ** 2
                         math.sqrt(bone_2[0] ** 2 + bone_2[1] ** 2))   #  + bone_2[2] ** 2
    # print(f"Lower product: {lower_dot_product}")  # this part is not a dot product, but whatever its just simplification

    dot_product = upper_dot_product / lower_dot_product
    # print(f"Dot product: {dot_product}")

    angle = math.acos(dot_product) * (180 / math.pi)
    return angle  # if this angle is not between 0 - 180, something is very wrong


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