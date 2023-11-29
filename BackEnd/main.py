# line 1, this is where it all begins
import pyzed.sl as sl
import cv2
import numpy as np

# Create a ZED camera
init_params = sl.InitParameters()
# init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Choose the appropriate depth mode
# init_params.depth_mode = sl.DEPTH_MODE.NEURAL

zed = sl.Camera()
if not zed.is_opened():
    print("Opening ZED Camera...")
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Failed to open ZED Camera")
        exit()

# Defines the keypoints of the skeleton
keypoints = ['Right_Foot', 'Left_Foot', 'Left_Knee', 'Right_Knee', 'Pelvis', 'Left_Hand', 'Right_Hand', 'Right_Elbow', 'Left_Elbow', 'Right_Shoulder', 'Left_Shoulder', 'Chest', 'Head']

# Orders the keypoints so that the head is ontop and the feet are at the bottom
keypoints_reordered = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# Define connections between keypoints with labels
skeleton_connections = [(9, 12, 'Pelvis and Left Knee'), (12, 13, 'Left Knee and Left Foot'),
                        (9, 10, 'Pelvis and Right Knee'), (10, 11, 'Right Knee and Right Foot'),
                        (2, 9, 'Chest and Pelvis'),
                        (6, 7, 'Left Shoulder and Left Elbow'), (7, 8, 'Left Elbow and Left Hand'),
                        (3, 4, 'Right Shoulder and Right Elbow'), (4, 5, 'Right Elbow and Right Hand'),
                        (2, 3, 'Chest and Right Shoulder'), (2, 6, 'Chest and Left Shoulder'),
                        (1, 2, 'Head and Chest')]

while True:
    # Capture a frame from the ZED camera
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve the RGB and depth images
        image = sl.Mat()
        zed.retrieve_image(image, sl.VIEW.LEFT)  # Retrieve the RGB image

        # Inside the loop, after retrieving the RGB image
        color_image = image.get_data()
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

        # Defines a list so the yellow centroids aka the yellow labels have a place to be stored
        yellow_centroids = []

        # Yellow color threshold in HSV values
        lower_yellow = np.array([20, 90, 180])
        upper_yellow = np.array([50, 255, 255])

        # Create a mask for yellow color
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        # Shows the yellow mask with all of the yellow picked up by the threshold
        cv2.imshow("Yellow mask before", yellow_mask)

        # filter for making yellow stuff be together
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_ELLIPSE, kernel3)
        yellow_mask_filter = cv2.morphologyEx(yellow_mask, cv2.MORPH_DILATE, kernel3)

        # The yellow/orange color thresholds area are detected based on size
        # if this line gives error write: _ , yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Doesn't do shit, but cant remove or else it wont work
        min_blob_area = 90
        max_blob_area = 100

        bloobers = []
        # technically this is supposed to filter out yellow contours that are not within the min/max blob area
        for yellow_contour in yellow_contours:
            area = cv2.contourArea(yellow_contour)
            if min_blob_area <= area <= max_blob_area:
                bloobers.append(yellow_contour)

        # The 2 below lines, creates a mask with the detected yellow contours from the for loop above and fills out the area around them
        pruned_mask = np.zeros_like(yellow_mask)
        # noinspection PyTypeChecker
        cv2.drawContours(pruned_mask, bloobers, -1, 255, thickness=cv2.FILLED)

        # another filtering step to make sure that if the area is 0 it is not detected
        filtered_yellow_contours = [contour for contour in yellow_contours if cv2.contourArea(contour)]

        # Draw rectangles around the detected yellow objects for some reason, this is also technically not needed, but break if removed
        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            cv2.rectangle(yellow_mask, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color, thickness 2

        # Calculates the center of the remaining yellow contours, and are stored in the yellow_centroids list
        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            centroid_x = x + w // 2
            centroid_y = y + h // 2
            yellow_centroids.append((centroid_x, centroid_y))

        # Sorts the yellow centroids by the y coordinates
        yellow_centroids_sorted = sorted(enumerate(yellow_centroids), key=lambda x: x[1][1])

        #makes the connections represent a skeleton-ish
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
                # _, means that the first variable in the turple is being ignores because we only want the x and y values.
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
        # Shows the raw image of the camera
        cv2.imshow("Segmented RGB with Tracked Yellow Objects", color_image)

        # Shows the yellow masks with the yellow centroids
        cv2.imshow("Tracking of Skeleton", yellow_mask)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the ZED camera and close OpenCV windows
zed.close()
cv2.destroyAllWindows()
# line 141 no more please