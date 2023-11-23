import numpy as np
import pyzed.sl as sl
import math
import Joints
from AngleDetection import points_to_bones

# Custom BODY_38_BONES
# Spinal cord
lower_spine =       points_to_bones(Joints.pelvis, Joints.lower_spine)
middle_spine =      points_to_bones(Joints.lower_spine, Joints.middle_spine)
upper_spine =       points_to_bones(Joints.middle_spine, Joints.upper_spine)
neck =              points_to_bones(Joints.upper_spine, Joints.neck)
nose =              points_to_bones(Joints.neck, Joints.nose)

# Face
left_eye =          points_to_bones(Joints.nose, Joints.left_eye)
right_eye =         points_to_bones(Joints.nose, Joints.right_eye)
left_ear =          points_to_bones(Joints.left_eye, Joints.left_ear)
right_ear =         points_to_bones(Joints.right_eye, Joints.right_ear)

# Left arm
left_clavicle =     points_to_bones(Joints.upper_spine, Joints.left_clavicle)
left_shoulder =     points_to_bones(Joints.left_clavicle, Joints.left_shoulder)
left_arm_upper =    points_to_bones(Joints.left_shoulder, Joints.left_elbow)
left_arm_lower =    points_to_bones(Joints.left_elbow, Joints.left_wrist)

# Right arm
right_clavicle =    points_to_bones(Joints.upper_spine, Joints.right_clavicle)
right_shoulder =    points_to_bones(Joints.right_clavicle, Joints.right_shoulder)
right_arm_upper =   points_to_bones(Joints.right_shoulder, Joints.right_elbow)
right_arm_lower =   points_to_bones(Joints.right_elbow, Joints.right_wrist)

# Left leg
left_hip =          points_to_bones(Joints.pelvis, Joints.left_hip)
left_leg_upper =    points_to_bones(Joints.left_hip, Joints.left_knee)
left_leg_lower =    points_to_bones(Joints.left_knee, Joints.left_ankle)

# Right leg
right_hip =         points_to_bones(Joints.pelvis, Joints.right_hip)
right_leg_upper =   points_to_bones(Joints.right_hip, Joints.right_knee)
right_leg_lower =   points_to_bones(Joints.right_knee, Joints.right_ankle)

# Left foot
left_foot_big_toe =      points_to_bones(Joints.left_ankle, Joints.left_big_toe)
left_foot_small_toe =    points_to_bones(Joints.left_ankle, Joints.left_small_toe)
left_foot_heel =         points_to_bones(Joints.left_ankle, Joints.left_heel)

# Right foot
right_foot_big_toe =     points_to_bones(Joints.right_ankle, Joints.right_big_toe)
right_foot_small_toe =   points_to_bones(Joints.right_ankle, Joints.right_small_toe)
right_foot_heel =        points_to_bones(Joints.right_ankle, Joints.right_heel)

# Left hand
left_hand_thumb =        points_to_bones(Joints.left_wrist, Joints.left_hand_thumb)
left_hand_index =        points_to_bones(Joints.left_wrist, Joints.left_hand_index)
left_hand_middle =       points_to_bones(Joints.left_wrist, Joints.left_hand_middle)
left_hand_pinky =        points_to_bones(Joints.left_wrist, Joints.left_hand_pinky)

# Right hand
right_hand_thumb =       points_to_bones(Joints.right_wrist, Joints.right_hand_thumb)
right_hand_index =       points_to_bones(Joints.right_wrist, Joints.right_hand_index)
right_hand_middle =      points_to_bones(Joints.right_wrist, Joints.right_hand_middle)
right_hand_pinky =       points_to_bones(Joints.right_wrist, Joints.right_hand_pinky)


# OpenPose Bones
# Spinal Cord
op_neck =               points_to_bones(Joints.op_nose, Joints.op_neck)
op_right_spine =        points_to_bones(Joints.op_neck, Joints.op_right_hip)
op_left_spine =         points_to_bones(Joints.op_neck, Joints.op_left_hip)

# Arms
op_right_clavicle =     points_to_bones(Joints.op_neck, Joints.op_right_shoulder)
op_right_upper_arm =    points_to_bones(Joints.op_right_shoulder, Joints.op_right_elbow)
op_right_lower_arm =    points_to_bones(Joints.op_right_elbow, Joints.op_right_wrist)
op_left_clavicle =      points_to_bones(Joints.op_neck, Joints.op_left_shoulder)
op_left_upper_arm =     points_to_bones(Joints.op_left_shoulder, Joints.op_left_elbow)
op_left_lower_arm =     points_to_bones(Joints.op_left_elbow, Joints.op_left_wrist)

# Legs
op_right_upper_leg =    points_to_bones(Joints.op_right_hip, Joints.op_right_knee)
op_right_lower_leg =    points_to_bones(Joints.op_right_knee, Joints.op_right_ankle)
op_left_upper_leg =     points_to_bones(Joints.op_left_hip, Joints.op_left_knee)
op_left_lower_leg =     points_to_bones(Joints.op_left_knee, Joints.op_left_ankle)
