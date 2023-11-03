import pyzed.sl as sl
import cv2

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
depth_threshold = 1500  # Adjust this value based on your desired distance (in millimeters)

while True:
    # Capture a frame from the ZED camera
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Retrieve the depth map
        depth_data = sl.Mat()
        zed.retrieve_measure(depth_data, sl.MEASURE.DEPTH)

        # Convert the depth map to a numpy array
        depth_image = depth_data.get_data()

        # Create a binary mask for foreground detection
        foreground_mask = (depth_image < depth_threshold).astype('uint8')

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel)
        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel)

        # Create a grayscale image for visualization
        grayscale_image = (foreground_mask * 255).astype('uint8')

        # Apply the mask to the depth image to extract the person
        segmented_depth = cv2.bitwise_and(depth_image, depth_image, mask=foreground_mask)

        # Display the segmented depth image
        cv2.imshow("Segmented Depth", segmented_depth)

        # Display the binary mask for visualization
        cv2.imshow("Foreground Mask", grayscale_image)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the ZED camera and close OpenCV windows
zed.close()
cv2.destroyAllWindows()