import cv2
import pandas as pd
import numpy as np
import csv
from obj_det import process_frames_and_detect
from get_depth import process_video
from get_frames import get_frames
# from det_human_pose import detect_human_pose
from test_3D import detect_car_pose
import math
from YOLO3D import inference

from ultrafastLaneDetector import UltrafastLaneDetector, ModelType
import os
model_path = "lanes/models/tusimple_18.pth"
model_type = ModelType.TUSIMPLE
use_gpu = False
lane_detector = UltrafastLaneDetector(model_path, model_type, use_gpu)


def create_csv(image, csv_path_object, csv_path_lane):
    columns = ["frame_index", "object_type", "bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2", "average_depth", "angle"]
    columns_lane = ["lane_num", "u","v","depth"]


    detections, output_frames_yolo = process_frames_and_detect(image)
    depth_map = process_video(image)

    for i in range(len(detections)):
        for j in range(i+1, len(detections)):
            if detections[i]['bbox'] == detections[j]['bbox']:
                if detections[i]['confidence'] > detections[j]['confidence']:
                    detections.pop(j)
                else:
                    detections.pop(i)
                break

    with open(csv_path_lane, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns_lane)  # Write the header

        output_img,lane_points = lane_detector.detect_lanes(image)



        #the returned lane points are for an image of size 1280x720 so we need to scale them to the original image size
        lane_points = [[(int(point[0]*image.shape[1]/1280), int(point[1]*image.shape[0]/720)) for point in lane] for lane in lane_points]

        #write the lane to the csv file and the depth
        for lane_num,lane in enumerate(lane_points):
            for i in range(len(lane)-1):
                point_depth = depth_map[int((lane[i][1]+lane[i+1][1])/2), int((lane[i][0]+lane[i+1][0])/2)]
                writer.writerow([lane_num, lane[i][0], lane[i][1], point_depth])
                

        
        

    with open(csv_path_object, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write the header


    
        image_resized = cv2.resize(image, (640, 640))

        try:

            alpha_list, theta_ray_list,box_2d_list = detect_car_pose(image_resized)
        


            for i in range(len(box_2d_list)):
                box_2d_list[i] = [[int(box_2d_list[i][0][0]*image.shape[1]/640), int(box_2d_list[i][0][1]*image.shape[0]/640)], [int(box_2d_list[i][1][0]*image.shape[1]/640), int(box_2d_list[i][1][1]*image.shape[0]/640)]]
        except:
             pass
        for detection in detections:
            bbox = detection['bbox']
            object_type = detection['object_type']



            # Extract depth for the object's bounding box area
            depth_area = depth_map[bbox[1]:bbox[3], bbox[0]:bbox[2]]


            depth_center = depth_map[int((bbox[1]+bbox[3])/2), int((bbox[0]+bbox[2])/2)]

            # if object_type == "person":
            #     img_person = image[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            #     candidate, subset = detect_human_pose(img_person)
            

            angle = 0
            alpha = 0
            theta_ray = 0
            try:
                if object_type == "car" or object_type == "truck" or object_type == "bus":
                
                
                
                    for i in range(len(box_2d_list)):
                        box = box_2d_list[i]
                        if abs(bbox[0] - box[0][0]) < 8 and abs(bbox[1] - box[0][1]) < 8 and abs(bbox[2] - box[1][0]) < 8 and abs(bbox[3] - box[1][1]) < 8:
                            alpha = alpha_list[i]
                            theta_ray = theta_ray_list[i]
                            break

                    angle= alpha + theta_ray
                
            except:
                pass
            
            #convert to degrees
            angle = math.degrees(angle)




             

            writer.writerow(['0', object_type, bbox[0], bbox[1], bbox[2], bbox[3], depth_center, angle])
           # writer.writerow(['0', object_type, bbox[0], bbox[1], bbox[2], bbox[3], average_depth, 0, 0])





    print(f"CSV file has been created at {csv_path_object}")




#go through all the images in the video_images folder
list_of_files = os.listdir('./video_images')


list_of_files.sort()
for file in list_of_files:
    image_path = './video_images/'+file
    image = cv2.imread(image_path)
    #change the name of the csv files and put them in folder object_csv and lane_csv
    #create object_csv and lane_csv folders
    if not os.path.exists('object_csv'):
        os.makedirs('object_csv')
    if not os.path.exists('lane_csv'):
        os.makedirs('lane_csv')
    create_csv(image, f"./object_csv/object_{file}.csv", f"./lane_csv/lane_{file}.csv")
