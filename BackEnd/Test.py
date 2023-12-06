import cv2
import numpy as np
import math
import time
import sys

# Create a VideoCapture object for the camera (0 for default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Helper function to calculate the angle
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Function to detect keypoints
def detect_keypoints(frame):
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([11, 77, 227])
    upper_yellow = np.array([22, 255, 255])
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))

    contours = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    centroids = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Threshold area
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centroids.append((cX, cY))
    return centroids

# Calibration phase
def calibrate():
    print("Calibration phase: Please position yourself in the frame.")
    calibration_keypoints = []
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            continue

        keypoints = detect_keypoints(frame)
        if len(keypoints) >= 3:
            calibration_keypoints = sorted(keypoints, key=lambda point: (point[0], point[1]))[:3]
            break

        cv2.putText(frame, "Calibrating...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

    print("Calibration successful.")
    return calibration_keypoints

calibration_keypoints = calibrate()

# Rep counting variables
rep_count = 0
arm_extended = False  # State to track if arm is extended

def main(exercise_time):
    global arm_extended, rep_count
    start_time = time.time()

    while time.time() - start_time < exercise_time:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        keypoints = detect_keypoints(frame)

        if len(keypoints) >= 3:
            keypoints_sorted = sorted(keypoints, key=lambda point: (point[0], point[1]))[:3]
            shoulder_point, elbow_point, hand_point = keypoints_sorted

            # Calculate the angle
            angle = calculate_angle(shoulder_point, elbow_point, hand_point)

            # Check if arm is extended
            if angle > 130:
                arm_extended = True

            # Check if arm is curled and was previously extended
            if arm_extended and angle <= 50:
                rep_count += 1
                arm_extended = False  # Reset the state

            # Display the angle and rep count
            cv2.putText(frame, f"Angle: {int(angle)}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Reps: {rep_count}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Draw the keypoints and connections
            for point in [shoulder_point, elbow_point, hand_point]:
                cv2.circle(frame, point, 5, (0, 255, 0), -1)
            cv2.line(frame, shoulder_point, elbow_point, (255, 0, 0), 3)
            cv2.line(frame, elbow_point, hand_point, (255, 0, 0), 3)
        else:
            cv2.putText(frame, "Keypoints not detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the frame
        cv2.imshow("Frame", frame)

        # Exit condition based on time elapsed
        if time.time() - start_time >= exercise_time:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Print the final rep count at the end of the exercise time
    print("Hello")
    print(rep_count)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--time':
        print("Usage: python script_name.py --time <exercise_time_in_seconds>")
        sys.exit(1)

    exercise_time = int(sys.argv[2])
    main(exercise_time)
