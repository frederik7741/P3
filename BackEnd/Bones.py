import numpy as np
import pyzed.sl as sl
import math
import Joints
from AngleDetection import points_to_bones

# Custom BODY_38_BONES
# Spinal cord
lower_spine =       points_to_bones(Joints.pelvis_joint, Joints.lower_spine_joint)
middle_spine =      points_to_bones(Joints.lower_spine_joint, Joints.middle_spine_joint)
upper_spine =       points_to_bones(Joints.middle_spine_joint, Joints.upper_spine_joint)
neck =              points_to_bones(Joints.upper_spine_joint, Joints.neck_joint)
nose =              points_to_bones(Joints.neck_joint, Joints.nose_joint)

# Face
nose_to_left_eye =  points_to_bones(Joints.nose_joint, Joints.left_eye_joint)
nose_to_right_eye = points_to_bones(Joints.nose_joint, Joints.right_eye_joint)
eye_to_ear_left =   points_to_bones(Joints.left_eye_joint, Joints.left_ear_joint)
eye_to_ear_right =  points_to_bones(Joints.right_eye_joint, Joints.right_ear_joint)

# Left arm
left_clavicle =     points_to_bones(Joints.upper_spine_joint, Joints.left_clavicle_joint)
left_shoulder =     points_to_bones(Joints.left_clavicle_joint, Joints.left_shoulder_joint)
left_arm_upper =    points_to_bones(Joints.left_shoulder_joint, Joints.left_elbow_joint)
left_arm_lower =    points_to_bones(Joints.left_elbow_joint, Joints.left_wrist_joint)

# Right arm
right_clavicle =    points_to_bones(Joints.upper_spine_joint, Joints.right_clavicle_joint)
right_shoulder =    points_to_bones(Joints.right_clavicle_joint, Joints.right_shoulder_joint)
right_arm_upper =   points_to_bones(Joints.right_shoulder_joint, Joints.right_elbow_joint)
right_arm_lower =   points_to_bones(Joints.right_elbow_joint, Joints.right_wrist_joint)

# Left leg
left_hip = points_to_bones(Joints.pelvis_joint, Joints.left_hip_joint)
left_upper_leg = points_to_bones(Joints.left_hip_joint, Joints.left_knee_joint)
left_lower_leg = points_to_bones(Joints.left_knee_joint, Joints.left_ankle_joint)

# Right leg
right_hip = points_to_bones(Joints.pelvis_joint, Joints.right_hip_joint)
right_upper_leg = points_to_bones(Joints.right_hip_joint, Joints.right_knee_joint)
right_lower_leg = points_to_bones(Joints.right_knee_joint, Joints.right_ankle_joint)

# Left foot
left_big_toe = points_to_bones(Joints.left_ankle_joint, Joints.left_big_toe_joint)
left_small_toe = points_to_bones(Joints.left_ankle_joint, Joints.left_small_toe_joint)
left_heel = points_to_bones(Joints.left_ankle_joint, Joints.left_heel_joint)

# Right foot
right_big_toe = points_to_bones(Joints.right_ankle_joint, Joints.right_big_toe_joint)
right_small_toe = points_to_bones(Joints.right_ankle_joint, Joints.right_small_toe_joint)
right_heel = points_to_bones(Joints.right_ankle_joint, Joints.right_heel_joint)

# Left hand
left_thumb = points_to_bones(Joints.left_wrist_joint, Joints.left_hand_thumb_joint)
left_index = points_to_bones(Joints.left_wrist_joint, Joints.left_hand_index_joint)
left_middle = points_to_bones(Joints.left_wrist_joint, Joints.left_hand_middle_joint)
left_pinky = points_to_bones(Joints.left_wrist_joint, Joints.left_hand_pinky_joint)

# Right hand
right_thumb = points_to_bones(Joints.right_wrist_joint, Joints.right_hand_thumb_joint)
right_index = points_to_bones(Joints.right_wrist_joint, Joints.right_hand_index_joint)
right_middle = points_to_bones(Joints.right_wrist_joint, Joints.right_hand_middle_joint)
right_pinky = points_to_bones(Joints.right_wrist_joint, Joints.right_hand_pinky_joint)
