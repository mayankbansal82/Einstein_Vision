import cv2

########## every frame ##############
def get_frames(video_path):
    """
    Generator function to yield frames from a video at a specified frame rate.

    :param video_path: Path to the video file.
    :param frame_rate: Number of frames to skip before yielding the next frame. 
                       frame_rate=1 yields every frame, frame_rate=2 yields every second frame, etc.
    :return: Yields frames from the video.
    """
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()
########## every frame ##############


########## every second(s) ##############
# def get_frames(video_path, every_second=True):
#     """
#     Generator function to yield frames from a video, possibly every second.
    
#     :param video_path: Path to the video file.
#     :param every_second: Whether to yield every frame or just one frame per second.
#     :return: Yields frames from the video.
#     """
#     cap = cv2.VideoCapture(video_path)
#     frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get the video's frame rate

#     # Calculate the number of frames to skip to get one frame per second
#     if every_second:
#         skip_frames = int(frame_rate)

#     frame_index = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # Skip to the next frame if not the right time yet
#         if every_second and frame_index % skip_frames != 0:
#             frame_index += 1
#             continue

#         yield frame
#         frame_index += 1

#     cap.release()
########## every second(s) ##############


####### every nth frame ######### 
# def get_frames(video_path, frame_interval=3):
#     """
#     Generator function to yield frames from a video at a specified interval.

#     :param video_path: Path to the video file.
#     :param frame_interval: Interval of frames to skip before yielding the next frame. 
#                            frame_interval=1 yields every frame, frame_interval=2 yields every second frame, etc.
#     :return: Yields frames from the video.
#     """
#     cap = cv2.VideoCapture(video_path)
#     frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get the video's frame rate
#     print(frame_rate)

#     # Calculate the number of frames to skip based on the specified interval
#     skip_frames = frame_interval

#     frame_index = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         # Skip frames according to the specified interval
#         if frame_index % skip_frames != 0:
#             frame_index += 1
#             continue

#         yield frame
#         frame_index += 1

#     cap.release()
####### every nth frame ######### 

# Example usage:
# video_path = 'path_to_your_video.mp4'
# for frame in get_frames(video_path):
#     # Do something with the frame
#     pass
