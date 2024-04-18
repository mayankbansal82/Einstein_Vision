import cv2
import numpy as np
from get_frames import get_frames

def process_frame_for_lane_detection(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using the Canny detector
    edges = cv2.Canny(blur, 50, 150)

    # Define a region of interest (ROI) for lane detection
    height, width = edges.shape
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (0, height * 0.8),
        (width, height * 0.8),
        (width, height),
        (0, height),
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)

    # Mask the edges image
    masked_edges = cv2.bitwise_and(edges, mask)

    # Use Hough Line Transformation to detect lines
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 50, np.array([]), minLineLength=100, maxLineGap=50)

    # Draw the lines on the frame
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

    return frame

def process_frames_and_detect(video_path):





    frame_with_lanes = process_frame_for_lane_detection(video_path)

    # Display the frame with lane detections
    cv2.imshow('Lane Detection', frame_with_lanes)

    cv2.waitKey(0)
    cv2.destroyAllWindows()




    # for frame in get_frames(video_path):  # Update get_frames if needed to match function definition
    #     # Process each frame for lane detection
    #     frame_with_lanes = process_frame_for_lane_detection(frame)

    #     # Display the frame with lane detections
    #     cv2.imshow('Lane Detection', frame_with_lanes)
        
    #     if cv2.waitKey(1) == ord('q'):  # Press 'q' to quit
    #         break

    # cv2.destroyAllWindows()


# Example usage
# video_path = '/Users/mayankbansal/Desktop/CV/P3Data/Sequences/scene3/Undist/2023-02-14_11-49-54-front_undistort.mp4'  # Update this path

image_path = "/Users/mayankbansal/Desktop/CV/EV/test_images/traf.jpg"
video_path = cv2.imread(image_path)

process_frames_and_detect(video_path)