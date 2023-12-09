import cv2
import numpy as np
import sys
import time
import argparse
import csv

def calculate_angle(pt1, pt2, pt3):
    vector1 = [pt1[0] - pt2[0], pt1[1] - pt2[1]]
    vector2 = [pt3[0] - pt2[0], pt3[1] - pt2[1]]

    dot_product = sum(p*q for p, q in zip(vector1, vector2))

    magnitude1 = sum(p**2 for p in vector1)**0.5
    magnitude2 = sum(p**2 for p in vector2)**0.5

    if magnitude1 * magnitude2 == 0:
        return 0
    return np.degrees(np.arccos(dot_product / (magnitude1 * magnitude2)))

def find_arm_keypoints(contour, median_x, median_y):
    wrist = max(contour, key=lambda p: p[0][0])[0]
    elbow = (median_x, median_y)
    top_point = min(contour, key=lambda p: p[0][1])[0]
    shoulder_y = top_point[1] + int((max(contour, key=lambda p: p[0][1])[0][1] - top_point[1]) * (1 / 9))
    shoulder = (top_point[0], shoulder_y)

    return shoulder, elbow, wrist

def draw_points_and_lines(frame, points):
    for i, point in enumerate(points):
        cv2.circle(frame, (point[0], point[1]), 5, (0, 0, 255), -1)
        cv2.putText(frame, f'{["Shoulder", "Elbow", "Wrist"][i]}', (point[0] + 10, point[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        if i < len(points) - 1:
            cv2.line(frame, (point[0], point[1]), (points[i + 1][0], points[i + 1][1]), (255, 0, 0), 2)

def calibrate_keypoints(cap, background, num_samples=30):
    print("Calibration starting in 7 seconds. Please stand in position.")
    print("CALIBRATION_START")
    cv2.waitKey(7000)
    contour_points = []

    for _ in range(num_samples):
        ret, frame = cap.read()

        if not ret:
            continue
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgMask = cv2.absdiff(background, gray_frame)
        _, fgMask = cv2.threshold(fgMask, 10, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel, iterations=2)
        fgMask = cv2.dilate(fgMask, kernel, iterations=3)
        contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        if contours:
            body_contour = max(contours, key=cv2.contourArea)
            contour_points.extend(body_contour)

    contour_xs = [point[0][0] for point in contour_points]
    contour_ys = [point[0][1] for point in contour_points]

    return int(np.median(contour_xs)), int(np.median(contour_ys))


def main(exercise_time, difficulty, csv_filename="rep_angles.csv"):

    exercise_time = 30

    # Set thresholds based on difficulty
    if difficulty == 'Mild':
        max_angle_for_rep = 70
        min_angle_for_rep = 140
        Succesful_rep = 120
    elif difficulty == 'Moderat':
        max_angle_for_rep = 70
        min_angle_for_rep = 130
        Succesful_rep = 110
    elif difficulty == 'Hårdt Ramt':
        max_angle_for_rep = 70
        min_angle_for_rep = 120
        Succesful_rep = 100
    else:
        # Default thresholds if difficulty is not recognized
        max_angle_for_rep = 70
        min_angle_for_rep = 150
        Succesful_rep = 130

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    ret, background = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        return

    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    median_x, median_y = calibrate_keypoints(cap, background)
    previous_angle, rep_count = 180, 0
    has_extended, wrist_extension_threshold = True, 90

    with open(csv_filename, mode='w', newline='') as csv_file:
        fieldnames = ['Rep', 'Time', 'Time_Diff_From_Last_Rep', 'Angle_Diff_From_Last_Rep', 'Highest_Angle', 'Contours_Count', 'Successful_Rep']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header to the CSV file
        writer.writeheader()

        start_time = time.time()
        rep_start_time = start_time  # Initialize the rep_start_time
        last_highest_angle = 0

        while time.time() - start_time < exercise_time:
            ret, frame = cap.read()
            if not ret:
                break

            # Initialize highest_angle and contours_count for each iteration
            highest_angle = 0
            contours_count = 0

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fgMask = cv2.absdiff(background, gray_frame)
            _, fgMask = cv2.threshold(fgMask, 10, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel, iterations=2)
            fgMask = cv2.dilate(fgMask, kernel, iterations=3)
            contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]

            # Count the number of contours in the current frame
            contours_count = len(contours)

            if contours:
                body_contour = max(contours, key=cv2.contourArea)
                shoulder, elbow, wrist = find_arm_keypoints(body_contour, median_x, median_y)
                elbow_angle = calculate_angle(shoulder, elbow, wrist)

                # Update highest_angle for the current iteration
                highest_angle = max(highest_angle, elbow_angle)
                print(elbow_angle)



                is_resting = elbow_angle > 160 and wrist[0] - median_x < wrist_extension_threshold
                elbow_angle_text = "Resting" if is_resting else f'Angle: {int(elbow_angle)} deg'
                cv2.putText(frame, elbow_angle_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                if has_extended and elbow_angle >= max_angle_for_rep and not is_resting:
                    has_extended = False

                if not has_extended and previous_angle > min_angle_for_rep and elbow_angle <= min_angle_for_rep:
                    rep_count += 1
                    has_extended = True

                    # Calculate the time passed since the last rep
                    time_since_last_rep = time.time() - rep_start_time
                    rep_start_time = time.time()  # Update rep_start_time for the next rep

                    # Calculate the time difference from the last rep
                    time_diff_from_last_rep = rep_start_time - start_time

                    successful_rep = elbow_angle > Succesful_rep

                    # Calculate the angle difference from the last rep
                    angle_diff_from_last_rep = highest_angle - last_highest_angle
                    last_highest_angle = highest_angle

                    print(f"Elbow Angle: {elbow_angle}, Successful Rep: {successful_rep}, "
                          f"Time since last rep: {time_since_last_rep}, Time diff from last rep: {time_diff_from_last_rep}, "
                          f"Angle diff from last rep: {angle_diff_from_last_rep}")

                    # Log the success status along with other information
                    writer.writerow({
                        'Rep': rep_count,
                        'Time': round(time_since_last_rep, 2),
                        'Time_Diff_From_Last_Rep': round(time_diff_from_last_rep, 2),
                        'Angle_Diff_From_Last_Rep': round(angle_diff_from_last_rep, 2),
                        'Highest_Angle': round(highest_angle, 2),
                        'Contours_Count': contours_count,
                        'Successful_Rep': 'Succesful' if successful_rep else 'Unsuccesful'
                    })

                elif has_extended and elbow_angle <= min_angle_for_rep:
                    has_extended = False

                previous_angle = elbow_angle
                draw_points_and_lines(frame, [shoulder, elbow, wrist])

            cv2.putText(frame, f'Reps: {rep_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Frame", frame)
            cv2.imshow("Foreground Mask", fgMask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print(rep_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--time', type=int, default=60, help='Exercise time in seconds')
    parser.add_argument('--difficulty', type=str, default='Mild', help='Difficulty level')
    args = parser.parse_args()

    main(args.time, args.difficulty)
