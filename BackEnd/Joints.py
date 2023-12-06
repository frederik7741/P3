import numpy as np
import math
# from AngleDetection import detected_body
# from YoloBodyDetection import datum
# from main import yellow_centroids_sorted  # importer keypoints fra kameraet

x = 0.0
y = 0.0
z = 0.0
# yellow_centroids_sorted = np.zeros((13, 2)) # slet den her linje (brugt til test)

head = 0.0, 0.0
chest = 0.0, 0.0

right_shoulder = 0.0, 0.0
right_elbow = 0.0, 0.0
right_hand = 0.0, 0.0
left_shoulder = 0.0, 0.0
left_elbow = 0.0, 0.0
left_hand = 0.0, 0.0

pelvis = 0.0, 0.0

right_knee = 0.0, 0.0
right_foot = 0.0, 0.0
left_knee = 0.0, 0.0
left_foot = 0.0, 0.0

joints_list = [head, chest,
              right_shoulder, right_elbow, right_hand,
              left_shoulder, left_elbow, left_hand,
              pelvis,
              right_knee, right_foot,
              left_knee, left_foot]


def random_coord():
    x = random_point()
    y = random_point()
    # z = random_point()
    return x, y  # , z

def random_point():
    return np.random.uniform(0, 90)

def get_joints_list():
    return joints_list

def set_joints_list(keypoint_list):
    index = 0
    for keypoint in keypoint_list:
        joints_list[index] = keypoint
        index += 1

def update_joints():
    test_index = 0
    for joints in range(13):
        # yellow_centroids_sorted[test_index] = random_coord()  # slet den her linje (brugt til test)
        joints_list[test_index] = yellow_centroids_sorted[test_index]
        # print(f"{test_index}: {joints_list[test_index]}")
        test_index += 1




