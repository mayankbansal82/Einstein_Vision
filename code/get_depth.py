import cv2
from get_frames import get_frames
import torch
import numpy as np
import matplotlib.pyplot as plt


# # frame_rate = 1 # Change frame_rate as needed

# for frame in get_frames(video_path):
#     # Process the frame
#     # For example, display the frame
#     cv2.imshow('Frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cv2.destroyAllWindows()

model_type="DPT_Hybrid"

def setup_midas(model_type):
    """
    Sets up and returns the MiDaS model and its transforms.
    
    :param model_type: Type of MiDaS model to use.
    :return: MiDaS model and the corresponding transforms.
    """
    midas = torch.hub.load("intel-isl/MiDaS", model_type)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    midas.to(device)
    midas.eval()

    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    if model_type in ["DPT_Large", "DPT_Hybrid"]:
        transform = midas_transforms.dpt_transform
    else:
        transform = midas_transforms.small_transform

    return midas, transform, device


def estimate_depth(frame, midas, transform, device):
    """
    Estimate depth for a single frame using MiDaS model.
    
    :param frame: The input frame for depth estimation.
    :param midas: The loaded MiDaS model.
    :param transform: The transform for preprocessing the input image.
    :param device: The device (CPU/GPU) to run the model on.
    :return: Depth estimation as a numpy array.
    """
    input_batch = transform(frame).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=frame.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth = prediction.cpu().numpy()
    return depth


def process_video(frame):
    midas, transform, device = setup_midas(model_type=model_type)

    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    depth_map = estimate_depth(frame, midas, transform, device)
    # print(depth_map.shape)
    # Normalize the depth map to be in the range 0-255
    depth_normalized = cv2.normalize(depth_map, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    depth_normalized_float = (depth_map - np.min(depth_map)) / (np.max(depth_map) - np.min(depth_map))

    return depth_normalized


# video_path = '/Users/mayankbansal/Desktop/CV/P3Data/Sequences/scene2/Undist/2023-03-03_10-31-11-front_undistort.mp4'
# for frame_index, frame in enumerate(get_frames(video_path)):
#     # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     depth_map = process_video(frame)
#     # print(depth_map)

#     cv2.imshow('Frame', frame)

#     plt.imshow(depth_map, cmap='gray')
#     plt.show(block=False)
#     plt.pause(1)
#     plt.close()