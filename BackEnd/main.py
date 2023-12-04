import cv2
import numpy as np
import Joints
import Exercises

# Create a VideoCapture object for the camera (0 for default camera)
cap = cv2.VideoCapture(2)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Defines the keypoints of the skeleton
keypoints = ['Hands', 'Elbows', 'Shoulder']

# Orders the keypoints so that the head is on top and the feet are at the bottom
keypoints_reordered = [1, 2, 3]


# Define connections between keypoints with labels
skeleton_connections = [(1, 2, 'Hand and Elbow'), (2, 3, 'Elbow and Shoulder')]

tracking_enabled = True

freeze_keypoints = False

while True:
    # Capture a frame from the camera
    ret, color_image = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Inside the loop, after retrieving the RGB image
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

    # Create a mask for yellow color
    yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

    # Shows the yellow mask with all of the yellow picked up by the threshold

    cv2.imshow("Yellow mask before", yellow_mask)
    # filter for making yellow stuff be together
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_ELLIPSE, kernel3)
    yellow_mask_filter = cv2.morphologyEx(yellow_mask, cv2.MORPH_DILATE, kernel3)
    yellow_mask_filter = cv2.morphologyEx(yellow_mask_filter, cv2.MORPH_OPEN, kernel3)
    cv2.imshow("Yellow mask after", yellow_mask_filter)

    # The yellow/orange color thresholds area are detected based on size
    yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Doesn't do anything, but can't remove or else it won't work
    min_blob_area = 90
    max_blob_area = 120

    bloobers = []
    # technically this is supposed to filter out yellow contours that are not within the min/max blob area
    for yellow_contour in yellow_contours:
        area = cv2.contourArea(yellow_contour)
        if min_blob_area <= area <= max_blob_area:
            bloobers.append(yellow_contour)

    # The 2 below lines create a mask with the detected yellow contours from the for loop above and fill out the area around them
    pruned_mask = np.zeros_like(yellow_mask)
    cv2.drawContours(pruned_mask, bloobers, -1, 255, thickness=cv2.FILLED)

    # another filtering step to make sure that if the area is 0 it is not detected
    filtered_yellow_contours = [contour for contour in yellow_contours if cv2.contourArea(contour)]

    # Draw rectangles around the detected yellow objects for some reason, this is also technically not needed, but breaks if removed
    for yellow_contour in filtered_yellow_contours:
        x, y, w, h = cv2.boundingRect(yellow_contour)
        cv2.rectangle(yellow_mask, (x, y), (x + w, y + h), (0, 255, 255), 5)  # Yellow color, thickness 2

        # Calculates the center of the remaining yellow contours and stores them in the yellow_centroids list
    if tracking_enabled and not freeze_keypoints:
        yellow_centroids = []
        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            centroid_x = x + w // 2
            centroid_y = y + h // 2
            yellow_centroids.append((centroid_x, centroid_y))

    if tracking_enabled and not freeze_keypoints:
        yellow_centroids_sorted = sorted(enumerate(yellow_centroids), key=lambda x: x[1][1])

    # makes the connections represent a skeleton-ish only if tracking is enabled
    if tracking_enabled:
        # makes the connections represent a skeleton-ish
        for connection in skeleton_connections:
            if len(connection) == 2:
                keypoint1, keypoint2 = connection
                label = f'{keypoint1} and {keypoint2}'
            elif len(connection) == 3:
                keypoint1, keypoint2, label = connection

        if keypoint1 in keypoints_reordered and keypoint2 in keypoints_reordered:
            index1 = keypoints_reordered.index(keypoint1)
            index2 = keypoints_reordered.index(keypoint2)

        if index1 < len(yellow_centroids_sorted) and index2 < len(yellow_centroids_sorted):
            # _, means that the first variable in the tuple is being ignored because we only want the x and y values.
            _, (x1, y1) = yellow_centroids_sorted[index1]
            _, (x2, y2) = yellow_centroids_sorted[index2]

            for index, (x, y) in yellow_centroids_sorted[:13]:
                if 0 <= index < len(keypoints):
                    # Draw a circle around the yellow object
                    cv2.circle(yellow_mask, (x, y), 5, (0, 255, 0), -1)  # Green color, filled circle

                    # Add label text
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(yellow_mask, keypoints[index], (x - 10, y - 10), font, 0.5, (255, 255, 255), 1,
                                cv2.LINE_AA)



    Joints.set_joints_list(yellow_centroids_sorted)
    Exercises.get_exercise_angles()

    # Shows the raw image of the camera
    cv2.imshow("Segmented RGB with Tracked Yellow Objects", color_image)

    # Shows the yellow masks with the yellow centroids
    cv2.imshow("Tracking of Skeleton", yellow_mask)

    print(freeze_keypoints)
    print(tracking_enabled)

    # Press 'q' to exit the loop
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # Press 's' to stop updating keypoints
        freeze_keypoints = not freeze_keypoints

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
