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
nose_eye_left =     find_angle(Bones.nose, Bones.left_eye)
nose_eye_right =    find_angle(Bones.nose, Bones.right_eye)
eye_ear_left =      find_angle(Bones.left_eye, Bones.left_ear)
eye_ear_right =     find_angle(Bones.right_eye, Bones.right_ear)

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
