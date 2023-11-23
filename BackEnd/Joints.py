import numpy as np
import pyzed.sl as sl
import math
# from AngleDetection import detected_body
from YoloBodyDetection import datum

# this is just a freestyle that probably does not work
detected_body = datum.poseKeypoints

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
