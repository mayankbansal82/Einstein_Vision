# import scipy.io

# # Load the .mat file
# mat_file_path = '/Users/mayankbansal/Desktop/CV/P3Data/Calib/calibration.mat'
# mat_data = scipy.io.loadmat(mat_file_path)

# # Print all the key names to inspect what's in there
# print(mat_data)


import cv2
import os

def save_frames(video_path, output_dir, skip_frames=0):
    """
    Extract frames from a video and save them as images.

    Parameters:
    - video_path: Path to the video file.
    - output_dir: Directory where images will be saved.
    - skip_frames: Number of frames to skip between saves.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % (skip_frames + 1) == 0:
            output_path = os.path.join(output_dir, f"frame{frame_count:04d}.jpg")
            cv2.imwrite(output_path, frame)
        
        frame_count += 1
    
    cap.release()
    print(f"Extracted {frame_count} frames.")

# Example usage
video_path = 'video.mp4'
output_dir = './video_images'
save_frames(video_path, output_dir, skip_frames=20)
