import numpy as np
import math
import Joints
from AngleDetection import points_to_bones

neck = [0.0, 0.0]

right_clavicle = [0.0, 0.0]
right_upper_arm = [0.0, 0.0]
right_lower_arm = [0.0, 0.0]
left_clavicle = [0.0, 0.0]
left_upper_arm = [0.0, 0.0]
left_lower_arm = [0.0, 0.0]

spine = [0.0, 0.0]

right_upper_leg = [0.0, 0.0]
right_lower_leg = [0.0, 0.0]
left_upper_leg = [0.0, 0.0]
left_lower_leg = [0.0, 0.0]

bones_list = [neck,
              right_clavicle, right_upper_arm, right_lower_arm,
              left_clavicle, left_upper_arm, left_lower_arm,
              spine,
              right_upper_leg, right_lower_leg,
              left_upper_leg, left_lower_leg]

def get_bones_list():
    return bones_list

def update_bones():
    Joints.update_joints()
    joints_list = Joints.get_joints_list()

    # Head
    bones_list[0] = points_to_bones(joints_list[0], joints_list[1])
    # Right arm
    bones_list[1] = points_to_bones(joints_list[1], joints_list[2])
    bones_list[2] = points_to_bones(joints_list[2], joints_list[3])
    bones_list[3] = points_to_bones(joints_list[3], joints_list[4])
    # Left arm
    bones_list[4] = points_to_bones(joints_list[1], joints_list[5])
    bones_list[5] = points_to_bones(joints_list[5], joints_list[6])
    bones_list[6] = points_to_bones(joints_list[6], joints_list[7])
    # Spine
    bones_list[7] = points_to_bones(joints_list[1], joints_list[8])
    # Right leg
    bones_list[8] = points_to_bones(joints_list[8], joints_list[9])
    bones_list[9] = points_to_bones(joints_list[9], joints_list[10])
    # Left leg
    bones_list[10] = points_to_bones(joints_list[8], joints_list[11])
    bones_list[11] = points_to_bones(joints_list[11], joints_list[12])


# ZED Keypoint
# neck = points_to_bones(Joints.head, Joints.chest)
#
# right_clavicle = points_to_bones(Joints.chest, Joints.right_shoulder)
# right_upper_arm = points_to_bones(Joints.right_shoulder, Joints.right_elbow)
# right_lower_arm = points_to_bones(Joints.right_elbow, Joints.right_hand)
# left_clavicle = points_to_bones(Joints.chest, Joints.left_shoulder)
# left_upper_arm = points_to_bones(Joints.left_shoulder, Joints.left_elbow)
# left_lower_arm = points_to_bones(Joints.left_elbow, Joints.left_hand)
#
# spine = points_to_bones(Joints.chest, Joints.pelvis)
#
# right_upper_leg = points_to_bones(Joints.pelvis, Joints.right_knee)
# right_lower_leg = points_to_bones(Joints.right_knee, Joints.right_foot)
# left_upper_leg = points_to_bones(Joints.pelvis, Joints.left_knee)
# left_lower_leg = points_to_bones(Joints.left_knee, Joints.left_foot)


# # Custom BODY_38_BONES
# # Spinal cord
# lower_spine =       points_to_bones(Joints.pelvis, Joints.lower_spine)
# middle_spine =      points_to_bones(Joints.lower_spine, Joints.middle_spine)
# upper_spine =       points_to_bones(Joints.middle_spine, Joints.upper_spine)
# neck =              points_to_bones(Joints.upper_spine, Joints.neck)
# nose =              points_to_bones(Joints.neck, Joints.nose)
#
# # Face
# left_eye =          points_to_bones(Joints.nose, Joints.left_eye)
# right_eye =         points_to_bones(Joints.nose, Joints.right_eye)
# left_ear =          points_to_bones(Joints.left_eye, Joints.left_ear)
# right_ear =         points_to_bones(Joints.right_eye, Joints.right_ear)
#
# # Left arm
# left_clavicle =     points_to_bones(Joints.upper_spine, Joints.left_clavicle)
# left_shoulder =     points_to_bones(Joints.left_clavicle, Joints.left_shoulder)
# left_arm_upper =    points_to_bones(Joints.left_shoulder, Joints.left_elbow)
# left_arm_lower =    points_to_bones(Joints.left_elbow, Joints.left_wrist)
#
# # Right arm
# right_clavicle =    points_to_bones(Joints.upper_spine, Joints.right_clavicle)
# right_shoulder =    points_to_bones(Joints.right_clavicle, Joints.right_shoulder)
# right_arm_upper =   points_to_bones(Joints.right_shoulder, Joints.right_elbow)
# right_arm_lower =   points_to_bones(Joints.right_elbow, Joints.right_wrist)
#
# # Left leg
# left_hip =          points_to_bones(Joints.pelvis, Joints.left_hip)
# left_leg_upper =    points_to_bones(Joints.left_hip, Joints.left_knee)
# left_leg_lower =    points_to_bones(Joints.left_knee, Joints.left_ankle)
#
# # Right leg
# right_hip =         points_to_bones(Joints.pelvis, Joints.right_hip)
# right_leg_upper =   points_to_bones(Joints.right_hip, Joints.right_knee)
# right_leg_lower =   points_to_bones(Joints.right_knee, Joints.right_ankle)
#
# # Left foot
# left_foot_big_toe =      points_to_bones(Joints.left_ankle, Joints.left_big_toe)
# left_foot_small_toe =    points_to_bones(Joints.left_ankle, Joints.left_small_toe)
# left_foot_heel =         points_to_bones(Joints.left_ankle, Joints.left_heel)
#
# # Right foot
# right_foot_big_toe =     points_to_bones(Joints.right_ankle, Joints.right_big_toe)
# right_foot_small_toe =   points_to_bones(Joints.right_ankle, Joints.right_small_toe)
# right_foot_heel =        points_to_bones(Joints.right_ankle, Joints.right_heel)
#
# # Left hand
# left_hand_thumb =        points_to_bones(Joints.left_wrist, Joints.left_hand_thumb)
# left_hand_index =        points_to_bones(Joints.left_wrist, Joints.left_hand_index)
# left_hand_middle =       points_to_bones(Joints.left_wrist, Joints.left_hand_middle)
# left_hand_pinky =        points_to_bones(Joints.left_wrist, Joints.left_hand_pinky)
#
# # Right hand
# right_hand_thumb =       points_to_bones(Joints.right_wrist, Joints.right_hand_thumb)
# right_hand_index =       points_to_bones(Joints.right_wrist, Joints.right_hand_index)
# right_hand_middle =      points_to_bones(Joints.right_wrist, Joints.right_hand_middle)
# right_hand_pinky =       points_to_bones(Joints.right_wrist, Joints.right_hand_pinky)
