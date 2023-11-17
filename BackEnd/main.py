import pyzed.sl as sl
import cv2
import numpy as np

# Create a ZED camera
init_params = sl.InitParameters()
init_params.depth_mode = sl.DEPTH_MODE.NEURAL  # Choose the appropriate depth mode
#init_params.depth_mode = sl.DEPTH_MODE.NEURAL

zed = sl.Camera()
if not zed.is_opened():
    print("Opening ZED Camera...")
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Failed to open ZED Camera")
        exit()

# Background subtraction parameters
min_depth_threshold = 1000  # Minimum depth threshold for 1 meter (in millimeters)
max_depth_threshold = 3000  # Maximum depth threshold for 2 meters (in millimeters)


#sets the Region Of Interest (ROI) to exclude the floor
roi_Height = 130
roi = (slice(0, -roi_Height), slice(None))

lower_Yellow = np.array([0,50,50], dtype=np.uint8)
upper_Yellow = np.array([30,255,255], dtype=np.uint8)

while True:
    # Capture a frame from the ZED camera
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve the RGB and depth images
        image = sl.Mat()
        zed.retrieve_image(image, sl.VIEW.LEFT)  # Retrieve the RGB image
        depth_data = sl.Mat()
        zed.retrieve_measure(depth_data, sl.MEASURE.DEPTH)  # Retrieve the depth map

        # Convert the depth map to a numpy array
        depth_image = depth_data.get_data()

        # Apply ROI to exclude the bottom part of the depth image
        depth_image_roi = depth_image[roi]

        # Create a binary mask for foreground detection based on the depth range
        foreground_mask = ((depth_image_roi >= min_depth_threshold) & (depth_image_roi <= max_depth_threshold)).astype('uint8')

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_ERODE, kernel2)
        for _ in range(4):
            foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel)

        # Find contours in the foreground mask
        contours, _ = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if there is at least one contour
        if contours:
            # Find the contour with the maximum area
            largest_contour = max(contours, key=cv2.contourArea)

            # Create an empty black image with the same size as the RGB image
            frame_with_contours = np.zeros_like(image.get_data(), dtype=np.uint8)

            # Draw only the largest contour
            cv2.drawContours(frame_with_contours, [largest_contour], -1, (0, 255, 0), 2)  # Green color, thickness 2

            # Display the RGB image with the largest contour
            cv2.imshow("Segmented RGB with Largest Contour", frame_with_contours)

        # Display the segmented depth image
        # cv2.imshow("Segmented Depth", depth_image)

        # Display the binary mask for visualization
        cv2.imshow("Foreground Mask", (foreground_mask * 255).astype('uint8'))

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the ZED camera and close OpenCV windows
zed.close()
cv2.destroyAllWindows()

# Main loop
"""while True:
    # Capture a new frame
    runtime_parameters = sl.RuntimeParameters()
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        # Retrieve the left image (color)
        left_image = sl.Mat()
        zed.retrieve_image(left_image, sl.VIEW.LEFT)

        # Retrieve the depth map
        depth_map = sl.Mat()
        zed.retrieve_measure(depth_map, sl.MEASURE.DEPTH)

        # Convert the images to formats suitable for OpenCV
        frame = left_image.get_data()
        depth_data = depth_map.get_data()

        # Apply color thresholding for yellow
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([20, 100, 100], dtype="uint8")
        upper_yellow = np.array([30, 255, 255], dtype="uint8")
        yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

        # Find contours in the binary mask
        contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw yellow points on the original frame within the depth range
        for contour in contours:
            # Check if the contour has non-zero points
            if len(contour) > 0:
                # Calculate the mean depth of the contour
                contour_depth = np.mean(depth_data[contour[:, 0, 1], contour[:, 0, 0]])

                # Filter based on depth thresholds
                if min_depth_threshold < contour_depth < max_depth_threshold:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the result
        cv2.imshow("Result", frame)

    # Break the loop when the 'ESC' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
zed.close()
cv2.destroyAllWindows()"""
