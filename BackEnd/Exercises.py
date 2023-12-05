import numpy as np
import math
import Angles

exercises = ["bicep_curls",
             "treadmill_walking",
             "reach_and_grasp",
             "standing_and_sitting",
             "step_ups"]

chosen_exercise = exercises[4]  # pick one of the 5 exercises (0 - 4)

important_angles = np.zeros(5)


def get_exercise_angles():
    Angles.update_angles()
    angle_list = Angles.get_angles_list()

    if chosen_exercise in ("bicep_curls", "reach_and_grasp"):
        important_angles[0] = angle_list[0]
        important_angles[1] = angle_list[1]
        important_angles[2] = angle_list[2]
        important_angles[3] = angle_list[3]
        important_angles[4] = angle_list[4]
    elif chosen_exercise in ("treadmill_walking", "standing_and_sitting", "step_ups"):
        important_angles[0] = angle_list[0]
        important_angles[1] = angle_list[5]
        important_angles[2] = angle_list[6]
        important_angles[3] = angle_list[7]
        important_angles[4] = angle_list[8]

    test_index = 0

    for angle in important_angles:
        important_angles[test_index] = angle
        print(f"{Angles.angle_names[test_index]}: {important_angles[test_index]}")
        test_index += 1

# # could probably make this alot simpler, like (upper/lower body), but whatever
# if chosen_exercise is bicep_curls:
#     important_angles.append(Angles.right_shoulder)  # maybe not
#     important_angles.append(Angles.right_elbow)
#     important_angles.append(Angles.left_shoulder)  # maybe not
#     important_angles.append(Angles.left_elbow)
# elif chosen_exercise is treadmill_walking:
#     important_angles.append(Angles.right_hip)
#     important_angles.append(Angles.right_knee)
#     important_angles.append(Angles.left_hip)
#     important_angles.append(Angles.left_knee)
# elif chosen_exercise is reach_and_grasp:
#     important_angles.append(Angles.neck)
#     important_angles.append(Angles.right_shoulder)
#     important_angles.append(Angles.right_elbow)
#     important_angles.append(Angles.left_shoulder)
#     important_angles.append(Angles.left_elbow)
# elif chosen_exercise is standing_and_sitting:
#     important_angles.append(Angles.neck)
#     important_angles.append(Angles.right_hip)
#     important_angles.append(Angles.right_knee)
#     important_angles.append(Angles.left_hip)
#     important_angles.append(Angles.left_knee)
# elif chosen_exercise is step_ups:
#     important_angles.append(Angles.neck)
#     important_angles.append(Angles.right_hip)
#     important_angles.append(Angles.right_knee)
#     important_angles.append(Angles.left_hip)
#     important_angles.append(Angles.left_knee)
