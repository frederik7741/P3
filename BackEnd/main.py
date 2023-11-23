import pyzed.sl as sl
import cv2
import numpy as np

# Create a ZED camera
init_params = sl.InitParameters()
init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Choose the appropriate depth mode
# init_params.depth_mode = sl.DEPTH_MODE.NEURAL

zed = sl.Camera()
if not zed.is_opened():
    print("Opening ZED Camera...")
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Failed to open ZED Camera")
        exit()


while True:
    # Capture a frame from the ZED camera
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve the RGB and depth images
        image = sl.Mat()
        zed.retrieve_image(image, sl.VIEW.LEFT)  # Retrieve the RGB image
        depth_data = sl.Mat()

        # Inside the loop, after retrieving the RGB image
        color_image = image.get_data()
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

        yellow_centroids = []

        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Yellow color threshold in HSV values
        lower_yellow = np.array([20, 90, 180])
        upper_yellow = np.array([50, 255, 255])

        # Create a mask for yellow color
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        cv2.imshow("Yellow mask before", yellow_mask)

        # filter for making yellow stuff be together
        yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_ELLIPSE, kernel3)
        yellow_mask_filter = cv2.morphologyEx(yellow_mask, cv2.MORPH_DILATE, kernel3)

        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_blob_area = 1
        max_blob_area = 100

        bloobers = []

        for yellow_contour in yellow_contours:
            area = cv2.contourArea(yellow_contour)
            if min_blob_area <= area <= max_blob_area:
                bloobers.append(yellow_contour)

        pruned_mask = np.zeros_like(yellow_mask)
        # noinspection PyTypeChecker
        cv2.drawContours(pruned_mask, bloobers, -1, 255, thickness=cv2.FILLED)

        # limiting the size
        filtered_yellow_contours = [contour for contour in yellow_contours if cv2.contourArea(contour)]

        # Draw rectangles around the detected yellow objects
        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            cv2.rectangle(yellow_mask, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color, thickness 2

        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            centroid_x = x + w // 2
            centroid_y = y + h // 2
            yellow_centroids.append((centroid_x, centroid_y))

            # Connect yellow objects with lines
        for i in range(len(yellow_contours) - 1):
            if i < len(yellow_centroids) - 1:
                x1, y1 = yellow_centroids[i]
                x2, y2 = yellow_centroids[i + 1]
                cv2.line(yellow_mask, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue color, thickness

        # yellow image
        cv2.imshow("Segmented RGB with Tracked Yellow Objects", color_image)

        cv2.imshow("YELLOW result tracking of squares", yellow_mask)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the ZED camera and close OpenCV windows
zed.close()
cv2.destroyAllWindows()