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
min_depth_threshold = 500  # Minimum depth threshold for 1 meter (in millimeters)
max_depth_threshold = 2000  # Maximum depth threshold for 2 meters (in millimeters)

min_contour_area = 100  # Adjust this threshold as needed
#max_contour_area = 200  # Adjust this threshold as needed


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

        # sets the Region Of Interest (ROI) to exclude the floor
        #Roi_width = 600
        #Roi_Floor = 130 + 100  # Exclude 130 pixels from the bottom and 100 pixels from the top

        #New_Width = image.get_width() - Roi_width
        #New_Height = image.get_height() - Roi_Floor

        # Calculate the ROI to achieve the desired width and height
        #roi = (slice(New_Height), slice(New_Width))

        # Apply ROI to the images
        #image_roi = image.get_data()[roi]
        #depth_image_roi = depth_image[roi]

        # Create a binary mask for foreground detection based on the depth range
        #foreground_mask = ((depth_image_roi >= min_depth_threshold) & (depth_image_roi <= max_depth_threshold)).astype('uint8')


        # Inside the loop, after retrieving the RGB image
        color_image = image.get_data()
        #color_image_roi = color_image[roi]
        #hsv_image = cv2.cvtColor(color_image_roi, cv2.COLOR_BGR2HSV)
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))

        #foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_ERODE, kernel2)



        """for _ in range(4):
            foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel)"""



        yellow_centroids = []

        color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        #Yellow color threshold in HSV values
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        #yellow color threshold in rgb values
        #lower_yellow = np.array([255, 255, 0], dtype="uint8")
        #upper_yellow = np.array([217, 217, 128], dtype="uint8")

        # Convert HSV to RGB for visualization
        #lower_yellow_rgb = cv2.cvtColor(np.uint8([[lower_yellow]]), cv2.COLOR_HSV2RGB)[0][0]
        #upper_yellow_rgb = cv2.cvtColor(np.uint8([[upper_yellow]]), cv2.COLOR_HSV2RGB)[0][0]



        # Create a mask for yellow color


        #cv2.imshow("HSV Image", hsv_image)
        #yellow_mask = ((depth_image >= min_depth_threshold) & (depth_image <= max_depth_threshold)).astype('uint8')

        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)

        #result_Image = cv2.bitwise_and(color_image_rgb, color_image_rgb, mask= yellow_mask)
        #cv2.imshow("resulttIamge", result_Image)

        cv2.imshow("Yellow mask before", yellow_mask)
        #yellow_mask_roi = yellow_mask[roi]
        #yellow_mask_filter = yellow_mask

        yellow_mask_filter = cv2.morphologyEx(yellow_mask, cv2.MORPH_ERODE, kernel3)
        #yellow_mask_filter_final = cv2.morphologyEx(yellow_mask_filter, cv2.MORPH_ELLIPSE, kernel3)
        #yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_ELLIPSE, kernel3)
       # for _ in range(4):
           # yellow_mask_filter2 = cv2.morphologyEx(yellow_mask, cv2.MORPH_DILATE, kernel3)
        #yellow_mask_filter = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel3)

        #yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_ELLIPSE, kernel3)
       #or _ in range(4):
       # yellow_mask_filter = cv2.morphologyEx(yellow_mask_filter2, cv2.MORPH_CLOSE, kernel3)

        #yellow_mask = cv2.morphologyEx(yellow_mask_roi, cv2.MORPH_DILATE, kernel3)
        #yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)

        #combined_mask = cv2.bitwise_and(foreground_mask, yellow_mask_roi)

        cv2.imshow("YELLOW", yellow_mask_filter)

        depth_filtered_yellow_mask = np.logical_and(depth_image >= min_depth_threshold, depth_image <= max_depth_threshold)
        yellow_mask = cv2.bitwise_and(yellow_mask, yellow_mask, mask=depth_filtered_yellow_mask.astype(np.uint8))

        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        min_blob_area = 30
        max_blob_area = 100

        bloobers = []

        for yellow_contour in yellow_contours:
            area = cv2.contourArea(yellow_contour)
            if min_blob_area <= area <= max_blob_area:
                bloobers.append(yellow_contour)

        pruned_mask = np.zeros_like(yellow_mask)
        cv2.drawContours(pruned_mask, bloobers, -1, 255, thickness=cv2.FILLED)


        #limiting the size
        filtered_yellow_contours = [contour for contour in yellow_contours if cv2.contourArea(contour) > min_contour_area]

        # Draw rectangles around the detected yellow objects
        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color, thickness 2

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
                cv2.line(color_image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue color, thickness

        #yellow_mask_colored = cv2.cvtColor(yellow_mask_roi, cv2.COLOR_GRAY2BGR)
        #result_image = cv2.addWeighted(color_image_roi, 1, yellow_mask_colored, 0.5, 0)

        # Find contours in the foreground mask

        #contours, _ = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


            # Find the contour with the maximum area
        #largest_contour = max(contours, key=cv2.contourArea)

        #frame_with_contours = np.zeros_like(image_roi, dtype=np.uint8)

        # Draw only the largest contour
        #cv2.drawContours(frame_with_contours, [largest_contour], -1, (0, 255, 0), 2)  # Green color, thickness 2

        #if min_contour_area < cv2.contourArea(largest_contour) < max_contour_area:
            # Create an empty black image with the same size as the RGB image

        #else:
            # If the largest contour does not meet the area thresholds, create an empty black image
        #    frame_with_contours = np.zeros_like(image_roi, dtype=np.uint8)

            # Create an empty black image with the same size as the RGB image
        #frame_with_contours = np.zeros_like(image.get_data(), dtype=np.uint8)

            # Draw only the largest contour
        #cv2.drawContours(frame_with_contours, [largest_contour], -1, (0, 255, 0), 2)  # Green color, thickness 2

        # Display the segmented depth image
        # cv2.imshow("Segmented Depth", depth_image)

        #cv2.imshow("Result", result_image)

        #yellow image
        cv2.imshow("Segmented RGB with Tracked Yellow Objects", color_image)

        # Display the RGB image with the largest contour
        #Black with green outline
        #cv2.imshow("Segmented RGB with Largest Contour", frame_with_contours)

        cv2.imshow("YELLOW result", yellow_mask)

        # Display the binary mask for visualization
        #Black and white
        #cv2.imshow("Foreground Mask", (foreground_mask * 255).astype('uint8'))

        #full image
        #cv2.imshow("Segmented RGB with Largest Contour and Tracked Yellow Labels", image.get_data())
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
