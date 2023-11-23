import numpy as np
import pyzed.sl as sl
import math
from AngleDetection import detected_body
from YoloBodyDetection import datum

# Custom BODY_38_PARTS
# Spinal Cord
pelvis =           detected_body.get_keypoint(0)
lower_spine =      detected_body.get_keypoint(1)
middle_spine =     detected_body.get_keypoint(2)
upper_spine =      detected_body.get_keypoint(3)
neck =             detected_body.get_keypoint(4)

# Face
nose =             detected_body.get_keypoint(5)
left_eye =         detected_body.get_keypoint(6)
right_eye =        detected_body.get_keypoint(7)
left_ear =         detected_body.get_keypoint(8)
right_ear =        detected_body.get_keypoint(9)

# Arms
left_clavicle =    detected_body.get_keypoint(10)
right_clavicle =   detected_body.get_keypoint(11)
left_shoulder =    detected_body.get_keypoint(12)
right_shoulder =   detected_body.get_keypoint(13)
left_elbow =       detected_body.get_keypoint(14)
right_elbow =      detected_body.get_keypoint(15)
left_wrist =       detected_body.get_keypoint(16)
right_wrist =      detected_body.get_keypoint(17)

# Legs
left_hip =         detected_body.get_keypoint(18)
right_hip =        detected_body.get_keypoint(19)
left_knee =        detected_body.get_keypoint(20)
right_knee =       detected_body.get_keypoint(21)
left_ankle =       detected_body.get_keypoint(22)
right_ankle =      detected_body.get_keypoint(23)

# Feet
left_big_toe =     detected_body.get_keypoint(24)
right_big_toe =    detected_body.get_keypoint(25)
left_small_toe =   detected_body.get_keypoint(26)
right_small_toe =  detected_body.get_keypoint(27)
left_heel =        detected_body.get_keypoint(28)
right_heel =       detected_body.get_keypoint(29)

# Hands
left_hand_thumb =  detected_body.get_keypoint(30)
right_hand_thumb = detected_body.get_keypoint(31)
left_hand_index =  detected_body.get_keypoint(32)
right_hand_index = detected_body.get_keypoint(33)
left_hand_middle = detected_body.get_keypoint(34)
right_hand_middle = detected_body.get_keypoint(35)
left_hand_pinky =  detected_body.get_keypoint(36)
right_hand_pinky = detected_body.get_keypoint(37)


# OpenPose Joints
# this is just a freestyle that probably does not work
op_body_parts = datum.poseKeypoints

# Spinal Cord
op_nose =              op_body_parts[0]
op_neck =              op_body_parts[1]

# Arms
op_right_shoulder =    op_body_parts[2]
op_right_elbow =       op_body_parts[3]
op_right_wrist =       op_body_parts[4]
op_left_shoulder =     op_body_parts[5]
op_left_elbow =        op_body_parts[6]
op_left_wrist =        op_body_parts[7]

# Legs
op_right_hip =         op_body_parts[8]
op_right_knee =        op_body_parts[9]
op_right_ankle =       op_body_parts[10]
op_left_hip =          op_body_parts[11]
op_left_knee =         op_body_parts[12]
op_left_ankle =        op_body_parts[13]

# Face
op_right_eye =         detected_body_parts[14]
op_left_eye =          detected_body_parts[15]
op_right_ear =         detected_body_parts[16]
op_left_ear =          detected_body_parts[17]
