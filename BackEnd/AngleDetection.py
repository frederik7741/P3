# for at regne vinklerne mellem led, definerer vi leddene som en 3D vektor og finder vinklen derimellem

import numpy as np
import pyzed.sl as sl
import math

body_param = sl.BodyTrackingParameters()
body_param.enable_tracking = True  # Track people across images flow
body_param.enable_body_fitting = True  # Smooth skeleton move
body_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_ACCURATE
body_param.body_format = sl.BODY_FORMAT.BODY_38  # Choose the BODY_FORMAT you wish to use


def points_to_joints(point_1, point_2):
    joint_length = [point_2[0] - point_1[0], point_2[1] - point_1[1], point_2[2] - point_1[2]]
    joint_origin = point_1
    joint = joint_length, joint_origin
    return joint


def find_angle(joint_1, joint_2):
    dot_product_upper = joint_1[0] * joint_2[0] + joint_1[1] * joint_2[1] + joint_1[2] * joint_2[2]
    print(f"Upper product: {dot_product_upper}")
    dot_product_lower = (math.sqrt(math.pow(joint_1[0], 2) + math.pow(joint_1[1], 2) + math.pow(joint_1[2], 2)) *
                         math.sqrt(math.pow(joint_2[0], 2) + math.pow(joint_2[1], 2) + math.pow(joint_2[2], 2)))
    print(f"Lower product: {dot_product_lower}")
    dot_product = dot_product_upper / dot_product_lower
    print(f"Dot product {dot_product}")
    angle = math.acos(dot_product) * 180 / math.pi
    return angle


coordinate_1 = [4, -3, 0]
coordinate_2 = [4, 2, 0]


print(f"coordinate_1: {coordinate_1}")
print(f"coordinate_2: {coordinate_2}")

print(f"Angle: {find_angle(coordinate_1, coordinate_2)}")
