# Einstein_Vision

## Project Overview

This project focuses on the detection and analysis of road scenes in video streams using advanced computer vision techniques and deep learning models. The main objectives include distinguishing between different objects on the road and pedestrians, determining their pose, integrate camera calibration for accurate 3D positioning in a simulated environment to recreate what we see on the Tesla's dashboard.

## Features

- **Vehicle Detection**: Utilize YOLOv8 for real-time vehicle detection.
- **Depth Estimation**: Utilize MiDaS for real-time depth estimation.
- **Vehicle pose estimation**: Utilize YOLO3D for vehicle pose estimation.
- **Human pose estimation**: Utilize YOLOv8 pose model for human pose estimation.
- **Lane Detection**: Utilize Ultrafast Lane detection model for lane detection.
- **Camera Calibration**: Apply camera calibration to convert image coordinates into 3D world coordinates using intrinsic and extrinsic parameters.

## Technologies Used

- **Python**: Primary programming language.
- **OpenCV**: For image processing and optical flow calculations.
- **PyTorch**: Utilized for running the YOLOv8 model for object detection.
- **Blender**: For visualizing the rendered scenes.

## Results
![Example Image](images/obj_det.gif "object detection")

Object Detection wih YOLOv8


![Example Image](images/3d_box.gif "object detection")

Vehicle Pose Estimation wih YOLO3D

![Example Image](images/midas.png "object detection")

Depth map from YOLO3D

![Example Image](images/human_pose.png "object detection")

Human pose estimation from YOLOv8 pose model

![Example Image](images/lane_net.png "object detection")
![Example Image](images/lane.png "object detection")

Lane detection from Ultrafast lane detection

![Example Image](images/blender_render.jpg "object detection")
![Example Image](images/image.jpg "object detection")
![Example Image](images/combined_image_newest.jpg "object detection")
![Example Image](images/combined_image.jpg "object detection")

Scene Recreation in Blender


