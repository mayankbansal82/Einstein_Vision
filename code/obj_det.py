import torch
import numpy as np
from get_frames import get_frames
import cv2
from ultralytics import YOLO
from PIL import Image
import os
# Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5m', pretrained=True)
model = YOLO("yolov8x.pt")

def process_frames_and_detect(frame):
    results = model.predict(frame)
    # Convert results to Pandas DataFrame for easier processing
    # detections_df = results.pandas().xyxy[0]  # Extract detections
    # print(len(results[0]))
    detections = results[0]
    # print(len(detections))

    # Prepare a list to hold processed detection data
    frame_detections = []

    # # Extract necessary information from detections
    # for index, row in detections_df.iterrows():
    #     detection_data = {
    #         "object_type": row['name'],
    #         "bbox": [int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])],
    #         "confidence": row['confidence']
    #     }
    #     frame_detections.append(detection_data)

    # # Return the processed detection data for the frame
    # return frame_detections, results

    for detection in detections:
        # print(detection.names[detection.boxes[0].cls[0].item()])
        detection_data = {
            "object_type": detection.names[detection.boxes[0].cls[0].item()], 
            "bbox": [int(detection.boxes[0].xyxy[0].tolist()[0]),int(detection.boxes[0].xyxy[0].tolist()[1]),int(detection.boxes[0].xyxy[0].tolist()[2]),int(detection.boxes[0].xyxy[0].tolist()[3])],
            "confidence": detection.boxes[0].conf[0].item() 
        }
        frame_detections.append(detection_data)
    
        # print(detection_data)

    return frame_detections, detections

# Example usage
# video_path = '/Users/mayankbansal/Desktop/CV/P3Data/Sequences/scene2/Undist/2023-03-03_10-31-11-front_undistort.mp4'  # Update this path

# for frame_index, frame in enumerate(get_frames(video_path)):
#     detections, results = process_frames_and_detect(frame)
#     # print(detections)
#     frame_with_detections = results.plot()[:,:,::-1]
#     cv2.imshow('YOLOv5 Object Detection', frame_with_detections)
#     if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit early
#         break
# cv2.destroyAllWindows()


# image_path = "video_images"
# for images in os.listdir(image_path):
#     video_path = cv2.imread(image_path + "/" + images)
#     detections, results = process_frames_and_detect(video_path)
#     frame_with_detections = results.plot()[:,:,::-1]
#     cv2.imshow('YOLOv5 Object Detection', frame_with_detections)
#     cv2.waitKey(0)
    
#     print(detections)


    