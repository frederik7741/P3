import cv2
import numpy as np
import Joints
import Exercises

# Create a VideoCapture object for the camera (0 for default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Defines the keypoints of the skeleton
keypoints = ['Hands', 'Elbows', 'Shoulder']

# Orders the keypoints so that the head is on top and the feet are at the bottom
keypoints_reordered = [3, 2, 1]


# Define connections between keypoints with labels
skeleton_connections = [(1, 2, 'Hand'), (2, 3, 'Elbow')]

while True:
    # Capture a frame from the camera
    ret, color_image = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Takes the color image and makes it HSV for better thresholding
    hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

    # Apply morphological operations to refine the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    # Defines a list so the yellow centroids aka the yellow labels have a place to be stored
    yellow_centroids = []

    # Yellow color threshold in HSV values
    lower_yellow = np.array([11, 77, 227])
    upper_yellow = np.array([22, 255, 255])

    # Create a mask for yellow color, that will later be displayed after some color thresholding
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # Shows the yellow mask with all the yellow picked up by the threshold

    cv2.imshow("Yellow mask before", yellow_mask)
    # filter for making yellow stuff be together
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_ELLIPSE, kernel3)
    yellow_mask_filter = cv2.morphologyEx(yellow_mask, cv2.MORPH_DILATE, kernel3)
    yellow_mask_filter = cv2.morphologyEx(yellow_mask_filter, cv2.MORPH_OPEN, kernel3)
    cv2.imshow("Yellow mask after", yellow_mask_filter)

    # The yellow/orange color thresholds area are detected based on size
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # filters the yellow_contours list with cv2.contourArea so anything that is non-zero is excluded
    filtered_yellow_contours = [contour for contour in yellow_contours if cv2.contourArea(contour)]

    # Calculate the center of the remaining yellow contours and stores them in the yellow_centroids list
    yellow_centroids = []
    for yellow_contour in filtered_yellow_contours:
        # cv2.boundingRect calculates the top-left conor, width and height of each yellow_contour in filtered_yellow_contours
        x, y, w, h = cv2.boundingRect(yellow_contour)
        # the 2 lines below, calculates the center of each yellow_contour, by adding half of the width to x and half of the height to y
        centroid_x = x + w // 2
        centroid_y = y + h // 2
        # stores the now calculated centroid coordinates to the yellow_centroid list.
        yellow_centroids.append((centroid_x, centroid_y))

    # Sorts the yellow centroids by the x coordinates for the Hand and y coordinates for Elbow and Shoulder
    yellow_centroids_sorted = sorted(enumerate(yellow_centroids), key=lambda x: (x[1][0], x[1][1], x[0]))

    # makes the connections represent a skeleton-ish
    for connection in skeleton_connections:
        # the below if statement checks is the length of the connections have 2 or 3 elements
        # if the length is 2 it makes a label, if its 3 the label is included
        if len(connection) == 2:
            keypoint1, keypoint2 = connection
            label = f'{keypoint1} and {keypoint2}'
        elif len(connection) == 3:
            keypoint1, keypoint2, label = connection

        # Find the indices(index in plural) of keypoints in the reordered list
        index1 = keypoints_reordered.index(keypoint1)
        index2 = keypoints_reordered.index(keypoint2)

        # Check if both keypoints are within the valid range, and can be attached to a yellow centroid sorted
        if index1 < len(yellow_centroids_sorted) and index2 < len(yellow_centroids_sorted):
            # Get the centroids for the keypoints
            _, (x1, y1) = yellow_centroids_sorted[index1]
            _, (x2, y2) = yellow_centroids_sorted[index2]

            # Draw the connection
            cv2.line(yellow_mask, (x1, y1), (x2, y2), (0, 255, 255), 2)

            # Add label text at the centroid of keypoint1
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(yellow_mask, label, (int(x1) - 10, int(y1) - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    Joints.set_joints_list(yellow_centroids_sorted)
    Exercises.get_exercise_angles()

    # Shows the raw image of the camera
    cv2.imshow("Segmented RGB with Tracked Yellow Objects", color_image)

    # Shows the yellow masks with the yellow centroids
    cv2.imshow("Tracking of Skeleton", yellow_mask)

    # Press 'q' to exit the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
