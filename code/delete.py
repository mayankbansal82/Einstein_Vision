#delete contents from the following folders object_csv, lane_csv, video_images, output_test

import os
import shutil

# List of folders to delete contents from
folders = ['object_csv', 'lane_csv', 'video_images', 'output_test']

for folder in folders:
    if os.path.exists(folder):
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"Folder {folder} does not exist.")

print("Contents of specified folders have been deleted.")