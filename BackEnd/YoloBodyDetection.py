import cv2
import torch  # need to install torch

from libs.yolov5.models.experimental import attempt_load  # YOLOv5 GitHub Repo in "libs" folder
from libs.yolov5.utils.general import non_max_suppression, scale_coords  # YOLOv5 GitHub Repo in "libs" folder
from libs.yolov5.utils.torch_utils import select_device  # YOLOv5 GitHub Repo in "libs" folder
from libs.openpose import pyopenpose as op  # OpenPose GitHub Repo in "libs" folder

# Load YOLOv8 model
device = select_device('')
model = attempt_load('yolov5s.pt', map_location=device)  # switch between: s, m, l, x to change model complexity
stride = int(model.stride.max())

# Configure OpenPose
params = {
    "model_folder": "BackEnd/libs/openpose-master/models/",
    "hand": False,
    "face": False,
    "number_people_max": 1
}

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# Set ZED2 camera parameters
zed = cv2.VideoCapture(0)  # Replace with Camera from main

while True:
    ### YOLO STUFF ###
    # Run YOLOv5 inference
    ret, frame = zed.read()

    # Run inference
    image = frame.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.transpose(2, 0, 1)
    image = image / 255.0
    image = torch.from_numpy(image).float().to(device)
    image = image.unsqueeze(0)

    predictions = model(image)[0]
    predictions = non_max_suppression(predictions, conf_thres=0.5, iou_thres=0.45)[0]

    # Draw bounding boxes
    if predictions is not None and len(predictions) > 0:
        predictions[:, :4] = scale_coords(image.shape[2:], predictions[:, :4], frame.shape).round()
        for det in predictions:
            # tl = Top Left, br = Bottom Right, conf = confidence, cls = class, det = detection
            tl, br, conf, cls = det[:4], det[4:8], det[8], int(det[9])
            cv2.rectangle(frame, tuple(map(int, tl)), tuple(map(int, br)), (0, 255, 0), 2)
            cv2.putText(frame, f'{model.names[cls]} {conf:.2f}', (int(tl[0]), int(tl[1] - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('YOLOv8 Object Detection', frame)

    ### OPENPOSE STUFF ###
    # Run OpenPose on the detected body
    datum = op.Datum()
    datum.cvInputData = frame
    opWrapper.emplaceAndPop([datum])

    # Extract keypoints from OpenPose output
    keypoints = datum.poseKeypoints[0]  # Assuming only one person is detected

    # Visualize keypoints (for demonstration)
    if keypoints is not None and len(keypoints) > 0:
        for point in keypoints:
            x, y = int(point[0]), int(point[1])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # probably thickness higher

    # Display the result
    cv2.imshow('Object Detection + Pose Estimation', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
zed.release()
cv2.destroyAllWindows()
