import cv2
import os

def create_video_from_images(image_folder, output_video_file, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()  # Sort the images by name

    # Determine the width and height from the first image
    image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(image_path)
    height, width, layers = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID'
    video = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

# Usage
image_folder = './video_images/'  # Path to the folder containing images
output_video_file = './output_video_og.mp4'  # Output video file
fps = 8  # Frames per second
create_video_from_images(image_folder, output_video_file, fps)

image_folder = './output_test/'  # Path to the folder containing images
output_video_file = './output_video.mp4'  # Output video file
fps = 8  # Frames per second
create_video_from_images(image_folder, output_video_file, fps)
