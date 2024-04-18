import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np

from pytorch_openpose.src import model
from pytorch_openpose.src import util
from pytorch_openpose.src.body import Body
# from pytorch_openpose.src.hand import Hand

body_estimation = Body('/Users/mayankbansal/Desktop/CV/EV/pytorch_openpose/model/body_pose_model.pth')
# hand_estimation = Hand('/Users/mayankbansal/Desktop/CV/EV/pytorch-openpose/model/hand_pose_model.pth')

def detect_human_pose(frame):
    candidate, subset = body_estimation(frame)
    print(candidate.shape)
    print(subset.shape)
    print(candidate)
    print(subset)
    return candidate, subset

image_path = '/Users/mayankbansal/Desktop/CV/EV/test_images/car5.jpg'
image = cv2.imread(image_path)
candidate, subset = detect_human_pose(image)
canvas = util.draw_bodypose(image, candidate, subset)

plt.imshow(canvas[:, :, [2, 1, 0]])
plt.axis('off')
plt.show()
