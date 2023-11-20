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

min_contour_area = 100  # Adjust this threshold as needed
max_contour_area = 200  # Adjust this threshold as needed


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
        Roi_width = 600
        Roi_Floor = 130 + 100  # Exclude 130 pixels from the bottom and 100 pixels from the top

        New_Width = image.get_width() - Roi_width
        New_Height = image.get_height() - Roi_Floor

        # Calculate the ROI to achieve the desired width and height
        roi = (slice(New_Height), slice(New_Width))
            #(image.get_width() - Roi_width) // 2, (image.get_width() + Roi_width) // 2))

        # Apply ROI to the images
        image_roi = image.get_data()[roi]
        depth_image_roi = depth_image[roi]

        # Create a binary mask for foreground detection based on the depth range
        foreground_mask = ((depth_image_roi >= min_depth_threshold) & (depth_image_roi <= max_depth_threshold)).astype('uint8')

        # Apply morphological operations to refine the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_ERODE, kernel2)




        for _ in range(4):
            foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_CLOSE, kernel)



        #eafjaef
            # Inside the loop, after retrieving the RGB image
        color_image = image.get_data()
        hsv_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

            # Define the range for yellow color in HSV
        lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
        upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

            # Create a mask for yellow color
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        yellow_mask_roi = yellow_mask[roi]

        combined_mask = cv2.bitwise_and(foreground_mask, yellow_mask_roi)

        yellow_contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #limiting the size
        filtered_yellow_contours = [contour for contour in yellow_contours if cv2.contourArea(contour) > min_contour_area]

        # Draw rectangles around the detected yellow objects
        for yellow_contour in filtered_yellow_contours:
            x, y, w, h = cv2.boundingRect(yellow_contour)
            cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color, thickness 2

            # Connect yellow objects with lines
        for i in range(len(yellow_contours) - 1):
            x1, y1, _, _ = cv2.boundingRect(yellow_contours[i])
            x2, y2, _, _ = cv2.boundingRect(yellow_contours[i + 1])

        # Draw a line between consecutive yellow objects
            cv2.line(color_image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Blue color, thickness


        # Find contours in the foreground mask
        contours, _ = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # New shit
       # color_image_roi = image.get_data()[roi]
        #hsv_image_roi = cv2.cvtColor(color_image_roi, cv2.COLOR_BGR2HSV)
        #yellow_labels_mask = cv2.inRange(hsv_image_roi, lower_Yellow, upper_Yellow)
        #foreground_mask_roi = foreground_mask  # Assuming the depth ROI is the same as the color ROI
        #combined_mask = cv2.bitwise_and(yellow_labels_mask, foreground_mask_roi)
        #yellow_contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        #new Shit
        # Check if there is at least one contour
        #if contours and yellow_contours:
           # for yellow_contour in yellow_contours[0]:

            # Find the contour with the maximum area
        largest_contour = max(contours, key=cv2.contourArea)

        if min_contour_area < cv2.contourArea(largest_contour) < max_contour_area:
            # Create an empty black image with the same size as the RGB image
            frame_with_contours = np.zeros_like(image_roi, dtype=np.uint8)

            # Draw only the largest contour
            cv2.drawContours(frame_with_contours, [largest_contour], -1, (0, 255, 0), 2)  # Green color, thickness 2



        else:
            # If the largest contour does not meet the area thresholds, create an empty black image
            frame_with_contours = np.zeros_like(image_roi, dtype=np.uint8)

            # Create an empty black image with the same size as the RGB image
        #frame_with_contours = np.zeros_like(image.get_data(), dtype=np.uint8)

            # Draw only the largest contour
        cv2.drawContours(frame_with_contours, [largest_contour], -1, (0, 255, 0), 2)  # Green color, thickness 2



            #new Shit
                #print(type(largest_contour), largest_contour.shape)
                #print(type(yellow_contours), yellow_contours[0][0].shape)
            #if cv2.pointPolygonTest(largest_contour, tuple(yellow_contour[0][0]), False) > 0:
            #        x, y, w, h = cv2.boundingRect(yellow_contour)
            #        cv2.rectangle(image.get_data(), (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color, thickness 2



        # Display the segmented depth image
        # cv2.imshow("Segmented Depth", depth_image)

        #yellow image
        cv2.imshow("Segmented RGB with Tracked Yellow Objects", color_image)

        # Display the RGB image with the largest contour
        #Black with green outline
        cv2.imshow("Segmented RGB with Largest Contour", frame_with_contours)

        # Display the binary mask for visualization
        #Black and white
        cv2.imshow("Foreground Mask", (foreground_mask * 255).astype('uint8'))

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
