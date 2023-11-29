import numpy as np
import pyzed.sl as sl
import math
import Angles

exercises = [bicep_curls,
             treadmill_walking,
             reach_and_grasp,
             standing_and_sitting,
             step_ups]

chosen_exercise = exercises[0]  # pick one of the 5 exercises (0 - 4)

important_angles = []

# could probably make this alot simpler, like (upper/lower body), but whatever
if chosen_exercise is bicep_curls:
    important_angles.append(Angles.right_shoulder)  # maybe not
    important_angles.append(Angles.right_elbow)
    important_angles.append(Angles.left_shoulder)  # maybe not
    important_angles.append(Angles.left_elbow)
elif chosen_exercise is treadmill_walking:
    important_angles.append(Angles.right_hip)
    important_angles.append(Angles.right_knee)
    important_angles.append(Angles.left_hip)
    important_angles.append(Angles.left_knee)
elif chosen_exercise is reach_and_grasp:
    important_angles.append(Angles.neck)
    important_angles.append(Angles.right_shoulder)
    important_angles.append(Angles.right_elbow)
    important_angles.append(Angles.left_shoulder)
    important_angles.append(Angles.left_elbow)
elif chosen_exercise is standing_and_sitting:
    important_angles.append(Angles.neck)
    important_angles.append(Angles.right_hip)
    important_angles.append(Angles.right_knee)
    important_angles.append(Angles.left_hip)
    important_angles.append(Angles.left_knee)
elif chosen_exercise is step_ups:
    important_angles.append(Angles.neck)
    important_angles.append(Angles.right_hip)
    important_angles.append(Angles.right_knee)
    important_angles.append(Angles.left_hip)
    important_angles.append(Angles.left_knee)

while True:
    index = 0

    for angle in important_angles:
        important_angles[index] = angle
        print(f"important_angles[{index}]: {important_angles[index]}")
        index += 1
