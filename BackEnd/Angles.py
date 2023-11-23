import numpy as np
import pyzed.sl as sl
import math
import Bones
from AngleDetection import find_angle

# Predefining angles
# Spinal Cord
pelvis_left_hip =               find_angle(Bones.lower_spine, Bones.left_hip)
pelvis_right_hip =              find_angle(Bones.lower_spine, Bones.right_hip)
lower_spine =                   find_angle(Bones.lower_spine, Bones.middle_spine)
middle_spine =                  find_angle(Bones.middle_spine, Bones.upper_spine)
upper_spine =                   find_angle(Bones.upper_spine, Bones.neck)
upper_spine_left_clavicle =     find_angle(Bones.upper_spine, Bones.left_clavicle)
upper_spine_right_clavicle =    find_angle(Bones.upper_spine, Bones.right_clavicle)
neck =                          find_angle(Bones.upper_spine, Bones.nose)
neck_left_clavicle =            find_angle(Bones.neck, Bones.left_clavicle)
neck_right_clavicle =           find_angle(Bones.neck, Bones.right_clavicle)

# Face
left_nose_eye =     find_angle(Bones.nose, Bones.left_eye)
right_nose_eye =    find_angle(Bones.nose, Bones.right_eye)
left_eye_ear =      find_angle(Bones.left_eye, Bones.left_ear)
right_eye_ear =     find_angle(Bones.right_eye, Bones.right_ear)

# Left Arm
left_clavicle =     find_angle(Bones.left_clavicle, Bones.left_shoulder)
left_shoulder =     find_angle(Bones.left_shoulder, Bones.left_arm_upper)
left_elbow =        find_angle(Bones.left_arm_upper, Bones.left_arm_lower)
left_wrist =        find_angle(Bones.left_arm_lower, Bones.left_hand_middle)

# Right Arm
right_clavicle =    find_angle(Bones.right_clavicle, Bones.right_shoulder)
right_shoulder =    find_angle(Bones.right_shoulder, Bones.right_arm_upper)
right_elbow =       find_angle(Bones.right_arm_upper, Bones.right_arm_lower)
right_wrist =       find_angle(Bones.right_arm_lower, Bones.right_hand_middle)

# Left Leg
left_hip =          find_angle(Bones.left_hip, Bones.left_leg_upper)
left_knee =         find_angle(Bones.left_leg_upper, Bones.left_leg_lower)
left_ankle =        find_angle(Bones.left_leg_lower, Bones.left_foot_big_toe)

# Right Leg
right_hip =         find_angle(Bones.right_hip, Bones.right_leg_upper)
right_knee =        find_angle(Bones.right_leg_upper, Bones.right_leg_lower)
right_ankle =       find_angle(Bones.right_leg_lower, Bones.right_foot_big_toe)

# Left Foot
left_foot_big_toe =     find_angle(Bones.left_foot_big_toe, Bones.left_leg_lower)
left_foot_small_toe =   find_angle(Bones.left_foot_small_toe, Bones.left_leg_lower)
left_foot_heel =        find_angle(Bones.left_foot_heel, Bones.left_leg_lower)

# Right Foot
right_foot_big_toe =    find_angle(Bones.right_foot_big_toe, Bones.right_leg_lower)
right_foot_small_toe =  find_angle(Bones.right_foot_small_toe, Bones.right_leg_lower)
right_foot_heel =       find_angle(Bones.right_foot_heel, Bones.right_foot_heel)

# Left Hand
left_hand_thumb =       find_angle(Bones.left_hand_thumb, Bones.left_arm_lower)
left_hand_index =       find_angle(Bones.left_hand_index, Bones.left_arm_lower)
left_hand_middle =      find_angle(Bones.left_hand_middle, Bones.left_arm_lower)
left_hand_pinky =       find_angle(Bones.left_hand_pinky, Bones.left_arm_lower)

# Right Hand
right_hand_thumb =      find_angle(Bones.right_hand_thumb, Bones.right_arm_lower)
right_hand_index =      find_angle(Bones.right_hand_index, Bones.right_arm_lower)
right_hand_middle =     find_angle(Bones.right_hand_middle, Bones.right_arm_lower)
right_hand_pinky =      find_angle(Bones.right_hand_pinky, Bones.right_arm_lower)


# OpenPose angles
# Spinal Cord
op_right_neck =     find_angle(Bones.op_neck, Bones.op_right_clavicle)
op_left_neck =      find_angle(Bones.op_neck, Bones.op_left_clavicle)
op_right_spine =    find_angle(Bones.op_neck, Bones.op_right_spine)
op_left_spine =     find_angle(Bones.op_neck, Bones.op_left_spine)

# Arms
op_right_shoulder = find_angle(Bones.op_right_clavicle, Bones.op_right_upper_arm)
op_right_elbow =    find_angle(Bones.op_right_upper_arm, Bones.op_right_lower_arm)
op_left_shoulder =  find_angle(Bones.op_left_clavicle, Bones.op_left_upper_arm)
op_left_elbow =     find_angle(Bones.op_left_upper_arm, Bones.op_left_lower_arm)

# Legs
op_right_hip =      find_angle(Bones.op_right_spine, Bones.op_right_upper_leg)
op_right_knee =     find_angle(Bones.op_right_upper_leg, Bones.op_right_lower_leg)
op_left_hip =       find_angle(Bones.op_left_spine, Bones.op_left_upper_leg)
op_left_knee =      find_angle(Bones.op_left_upper_leg, Bones.op_left_lower_leg)
