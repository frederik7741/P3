import pyzed.sl as sl
import cv2
import numpy as np

# Create a ZED camera
init_params = sl.InitParameters()
init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # Choose the appropriate depth mode
zed = sl.Camera()
if not zed.is_opened():
    print("Opening ZED Camera...")
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Failed to open ZED Camera")
        exit()

# Background subtraction parameters
min_depth_threshold = 1000  # Minimum depth threshold for 1 meter (in millimeters)
max_depth_threshold = 2000  # Maximum depth threshold for 2 meters (in millimeters)

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

        # Create a binary mask for foreground detection based on the depth range
        foreground_mask = ((depth_image >= min_depth_threshold) & (depth_image <= max_depth_threshold)).astype('uint8')

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_ERODE, kernel2)
        for _ in range(3):
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