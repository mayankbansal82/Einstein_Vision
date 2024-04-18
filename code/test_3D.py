import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np
import argparse
from pathlib import Path
import sys
import os

from YOLO3D import inference

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

# Create the parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument('--weights', type=str, default='yolov5m.pt', help='Path to the weights file')
parser.add_argument('--source', type=str, default='./test_images/car1.jpg', help='Path to the source image or video')
parser.add_argument('--reg_weights', type=str, default='./YOLO3D/weights/resnet18.pkl', help='Path to the regression weights file')
parser.add_argument('--model_select', type=str, default='resnet18', help='Model selection')
parser.add_argument('--output_path', type=str, default='./output_test', help='Path to save the output')
parser.add_argument('--save_result', action='store_true', help='Save the result')
parser.add_argument('--show_result', action='store_true', help='Show Results with imshow')
parser.add_argument('--calib_file', type=str, default=ROOT / './YOLO3D/eval/camera_cal/calib_cam_to_cam.txt', help='Calibration file or path')


# Parse the arguments
args = parser.parse_args()

# Access the arguments
weights = args.weights
source = args.source
reg_weights = args.reg_weights
model_select = args.model_select
output_path = args.output_path
save_result = args.save_result
show_result = args.show_result

def detect_car_pose(frame):
    alpha_list, theta_ray_list,box2d_list = inference.detect3d(
        reg_weights=args.reg_weights,
        model_select=args.model_select,
        source_img=frame,
        calib_file=args.calib_file,
        show_result="False",
        save_result=args.save_result,
        output_path=args.output_path
    )

    return alpha_list, theta_ray_list,box2d_list

if __name__ == "__main__":
    image_path = './video_images/frame0968.jpg'
    #iterate over all images in the video_images folder
    image = cv2.imread(image_path)
        #resize to 640x640
    image = cv2.resize(image, (640, 640))
    alpha, theta_ray,box_2d = detect_car_pose(image)
    
    # list_of_files = os.listdir('./video_images')
    # #sort the list of files
    # list_of_files.sort()
    # for file in list_of_files:
    #     image_path = './video_images/'+file
    #     image = cv2.imread(image_path)
    #     #resize to 640x640
    #     image = cv2.resize(image, (640, 640))
    #     alpha, theta_ray,box_2d = detect_car_pose(image)

    #     print("alpha: ",alpha)
    #     print("theta_ray: ",theta_ray)
    # image_path = './video_images/frame1984.jpg'
    # image = cv2.imread(image_path)
    # #resize to 640x640
    # image = cv2.resize(image, (640, 640))
    # alpha, theta_ray = detect_car_pose(image)

    # print("alpha: ",alpha)
    # print("theta_ray: ",theta_ray)
    # print("done!!")