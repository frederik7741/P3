import numpy as np
import pyzed.sl as sl
import math
from AngleDetection import detected_body

# Custom BODY_38_PARTS
# Spinal Cord
pelvis_joint =           detected_body.get_keypoint(0)
lower_spine_joint =      detected_body.get_keypoint(1)
middle_spine_joint =     detected_body.get_keypoint(2)
upper_spine_joint =      detected_body.get_keypoint(3)

# Face
neck_joint =             detected_body.get_keypoint(4)
nose_joint =             detected_body.get_keypoint(5)
left_eye_joint =         detected_body.get_keypoint(6)
right_eye_joint =        detected_body.get_keypoint(7)
left_ear_joint =         detected_body.get_keypoint(8)
right_ear_joint =        detected_body.get_keypoint(9)

# Arms
left_clavicle_joint =    detected_body.get_keypoint(10)
right_clavicle_joint =   detected_body.get_keypoint(11)
left_shoulder_joint =    detected_body.get_keypoint(12)
right_shoulder_joint =   detected_body.get_keypoint(13)
left_elbow_joint =       detected_body.get_keypoint(14)
right_elbow_joint =      detected_body.get_keypoint(15)
left_wrist_joint =       detected_body.get_keypoint(16)
right_wrist_joint =      detected_body.get_keypoint(17)

# Legs
left_hip_joint =         detected_body.get_keypoint(18)
right_hip_joint =        detected_body.get_keypoint(19)
left_knee_joint =        detected_body.get_keypoint(20)
right_knee_joint =       detected_body.get_keypoint(21)
left_ankle_joint =       detected_body.get_keypoint(22)
right_ankle_joint =      detected_body.get_keypoint(23)

# Feet
left_big_toe_joint =     detected_body.get_keypoint(24)
right_big_toe_joint =    detected_body.get_keypoint(25)
left_small_toe_joint =   detected_body.get_keypoint(26)
right_small_toe_joint =  detected_body.get_keypoint(27)
left_heel_joint =        detected_body.get_keypoint(28)
right_heel_joint =       detected_body.get_keypoint(29)

# Hands
left_hand_thumb_joint =  detected_body.get_keypoint(30)
right_hand_thumb_joint = detected_body.get_keypoint(31)
left_hand_index_joint =  detected_body.get_keypoint(32)
right_hand_index_joint = detected_body.get_keypoint(33)
left_hand_middle_joint = detected_body.get_keypoint(34)
right_hand_middle_joint = detected_body.get_keypoint(35)
left_hand_pinky_joint =  detected_body.get_keypoint(36)
right_hand_pinky_joint = detected_body.get_keypoint(37)
