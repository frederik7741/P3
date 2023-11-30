import numpy as np
import pyzed.sl as sl
import math
# from AngleDetection import detected_body
# from YoloBodyDetection import datum
from main import yellow_centroids_sorted  # importer keypoints fra kameraet

x = 0.0
y = 0.0
z = 0.0
# yellow_centroids_sorted = np.zeros((13, 3)) # slet den her linje (brugt til test)

head = 0.0, 0.0, 0.0
chest = 0.0, 0.0, 0.0

right_shoulder = 0.0, 0.0, 0.0
right_elbow = 0.0, 0.0, 0.0
right_hand = 0.0, 0.0, 0.0
left_shoulder = 0.0, 0.0, 0.0
left_elbow = 0.0, 0.0, 0.0
left_hand = 0.0, 0.0, 0.0

pelvis = 0.0, 0.0, 0.0

right_knee = 0.0, 0.0, 0.0
right_foot = 0.0, 0.0, 0.0
left_knee = 0.0, 0.0, 0.0
left_foot = 0.0, 0.0, 0.0

joints_list = [head, chest,
              right_shoulder, right_elbow, right_hand,
              left_shoulder, left_elbow, left_hand,
              pelvis,
              right_knee, right_foot,
              left_knee, left_foot]


def random_coord():
    x = random_point()
    y = random_point()
    z = random_point()
    return x, y, z

def random_point():
    return np.random.uniform(0, 90)

def get_joints_list():
    return joints_list


def update_joints():
    test_index = 0
    for joints in range(13):
        # yellow_centroids_sorted[test_index] = random_coord()  # slet den her linje (brugt til test)
        joints_list[test_index] = yellow_centroids_sorted[test_index]
        # print(f"{test_index}: {joints_list[test_index]}")
        test_index += 1

    # # ZED Keypoints
    # # index, body_part = yellow_centroids_sorted
    #
    # head = yellow_centroids_sorted[0]
    # chest = yellow_centroids_sorted[1]
    #
    # right_shoulder = yellow_centroids_sorted[2]
    # right_elbow = yellow_centroids_sorted[3]
    # right_hand = yellow_centroids_sorted[4]
    # left_shoulder = yellow_centroids_sorted[5]
    # left_elbow = yellow_centroids_sorted[6]
    # left_hand = yellow_centroids_sorted[7]
    #
    # pelvis = yellow_centroids_sorted[8]
    #
    # right_knee = yellow_centroids_sorted[9]
    # right_foot = yellow_centroids_sorted[10]
    # left_knee = yellow_centroids_sorted[11]
    # left_foot = yellow_centroids_sorted[12]


# # Custom BODY_38_PARTS
# # Spinal Cord
# pelvis =           detected_body.get_keypoint(0)
# lower_spine =      detected_body.get_keypoint(1)
# middle_spine =     detected_body.get_keypoint(2)
# upper_spine =      detected_body.get_keypoint(3)
# neck =             detected_body.get_keypoint(4)
#
# # Face
# nose =             detected_body.get_keypoint(5)
# left_eye =         detected_body.get_keypoint(6)
# right_eye =        detected_body.get_keypoint(7)
# left_ear =         detected_body.get_keypoint(8)
# right_ear =        detected_body.get_keypoint(9)
#
# # Arms
# left_clavicle =    detected_body.get_keypoint(10)
# right_clavicle =   detected_body.get_keypoint(11)
# left_shoulder =    detected_body.get_keypoint(12)
# right_shoulder =   detected_body.get_keypoint(13)
# left_elbow =       detected_body.get_keypoint(14)
# right_elbow =      detected_body.get_keypoint(15)
# left_wrist =       detected_body.get_keypoint(16)
# right_wrist =      detected_body.get_keypoint(17)
#
# # Legs
# left_hip =         detected_body.get_keypoint(18)
# right_hip =        detected_body.get_keypoint(19)
# left_knee =        detected_body.get_keypoint(20)
# right_knee =       detected_body.get_keypoint(21)
# left_ankle =       detected_body.get_keypoint(22)
# right_ankle =      detected_body.get_keypoint(23)
#
# # Feet
# left_big_toe =     detected_body.get_keypoint(24)
# right_big_toe =    detected_body.get_keypoint(25)
# left_small_toe =   detected_body.get_keypoint(26)
# right_small_toe =  detected_body.get_keypoint(27)
# left_heel =        detected_body.get_keypoint(28)
# right_heel =       detected_body.get_keypoint(29)
#
# # Hands
# left_hand_thumb =  detected_body.get_keypoint(30)
# right_hand_thumb = detected_body.get_keypoint(31)
# left_hand_index =  detected_body.get_keypoint(32)
# right_hand_index = detected_body.get_keypoint(33)
# left_hand_middle = detected_body.get_keypoint(34)
# right_hand_middle = detected_body.get_keypoint(35)
# left_hand_pinky =  detected_body.get_keypoint(36)
# right_hand_pinky = detected_body.get_keypoint(37)


