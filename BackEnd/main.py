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
max_depth_threshold = 2000  # Maximum depth threshold for 2 meters (in millimeters)

#sets the Region Of Interest (ROI) to exclude the floor
roi_Height = 130
roi = (slice(0, -roi_Height), slice(None))

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

        depth_image_roi = depth_image[roi]

        # Create a binary mask for foreground detection based on the depth range
        #foreground_mask = ((depth_image >= min_depth_threshold) & (depth_image <= max_depth_threshold)).astype('uint8')
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
            #frame_with_contours = np.zeros_like(image.get_data(), dtype=np.uint8)

            # Draw only the largest contour
            #cv2.drawContours(frame_with_contours, [largest_contour], -1, (0, 255, 0), 2)  # Green color, thickness 2

            # Display the RGB image with the largest contour
            #cv2.imshow("Segmented RGB with Largest Contour", frame_with_contours)

            if cv2.contourArea(largest_contour) > 1:

                hull = cv2.convexHull(largest_contour, returnPoints=True)

                if len(hull) >= 4 and len(largest_contour) >= 1000:
                    print(len(hull))
                    print(len(largest_contour))
                    print(f"contours er fucking dumme")
                    frame_with_contours = np.zeros_like(image.get_data(), dtype=np.uint8)

                    cv2.drawContours(frame_with_contours, [hull], -1, (0, 255, 0), 2)

                    defects = cv2.convexityDefects(largest_contour, cv2.convexHull(largest_contour, returnPoints=True))
                    if defects is not None:
                        for i in range(defects.shape[0]):
                            s,e,f, _ = defects[i,0]
                            start = tuple(largest_contour[s][0])
                            end = tuple(largest_contour[e][0])
                            far = tuple(largest_contour[f][0])

                            cv2.circle(frame_with_contours, far, 5, (0, 0, 255), -1)


                    cv2.imshow("Segmented RGB with Largest Contour", frame_with_contours)
                    print(f"fuck dig")
                    cv2.waitKey()


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