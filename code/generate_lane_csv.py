import cv2

from ultrafastLaneDetector import UltrafastLaneDetector, ModelType

model_path = "lanes/models/tusimple_18.pth"
model_type = ModelType.TUSIMPLE
use_gpu = False

image_path = "lanes/input.jpg"

# Initialize lane detection model
lane_detector = UltrafastLaneDetector(model_path, model_type, use_gpu)

# Read RGB images
img = cv2.imread(image_path, cv2.IMREAD_COLOR)



# Detect the lanes
output_img,lane_points = lane_detector.detect_lanes(img)





#the returned lane points are for an image of size 1280x720 so we need to scale them to the original image size
lane_points = [[(int(point[0]*img.shape[1]/1280), int(point[1]*img.shape[0]/720)) for point in lane] for lane in lane_points]

#draw the lanes
for lane in lane_points:
    for i in range(len(lane)-1):
        cv2.line(img, (lane[i][0], lane[i][1]), (lane[i+1][0], lane[i+1][1]), (0, 255, 0), 5)


print(lane_points)
# Draw estimated depth
cv2.namedWindow("Detected lanes", cv2.WINDOW_NORMAL) 
cv2.imshow("Detected lanes", img)
cv2.waitKey(0)

cv2.imwrite("output.jpg",output_img)