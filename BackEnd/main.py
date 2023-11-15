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

    #if cv2.contourArea(largest_contour) > 1:
    #            if len(largest_contour) >=3:
    #                epsilon = 0.01* cv2.arcLength(largest_contour, True)
    #                approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

                    #hull = cv2.convexHull(largest_contour, returnPoints=False)

                    #if len(hull) >= 3:

                        # Ensure the indices are within bounds
     #                   valid_indices = (hull[:, 0] < len(approx_contour))
      #                  hull_points = approx_contour[hull[valid_indices, 0]]

       #                 if len(hull_points) >= 3:
        #                    frame_with_contours = np.zeros_like(image.get_data(), dtype=np.uint8)
         #                   cv2.drawContours(frame_with_contours, [hull_points], -1, (0, 255, 0), 2)

                            # Manually calculate convexity defects
#                            hull_indices = hull[valid_indices, 0]
  #                          defects = []
 #                           for i in range(1, len(hull_indices) - 1):
   #                             start = hull_indices[i - 1]
    #                            end = hull_indices[i + 1]
     #                           farthest = hull_indices[i]

      #                          defects.append([start, end, farthest, 0])

       #                     defects = np.array(defects)

        #                    if defects is not None:
         #                       for defect in defects:
          #                          s, e, f, _ = defect
           #                         start = tuple(approx_contour[s][0])
            #                        end = tuple(approx_contour[e][0])
             #                       far = tuple(approx_contour[f][0])

              #              cv2.circle(frame_with_contours, far, 5, (0, 0, 255), -1)

               #             cv2.imshow("Segmented RGB with Largest Contour", frame_with_contours)
                #            cv2.waitKey(1)


        # Display the segmented depth image
            #cv2.imshow("Segmented Depth", depth_image)

        # Display the binary mask for visualization
     #       cv2.imshow("Foreground Mask", (foreground_mask * 255).astype('uint8'))

    # Press 'q' to exit the loop
    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   break

# Release the ZED camera and close OpenCV windows
#zed.close()
#cv2.destroyAllWindows()