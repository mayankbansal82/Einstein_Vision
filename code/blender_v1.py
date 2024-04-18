import bpy
import csv
import os
import numpy as np
from mathutils import Vector
import time
import math

fx = 1594.7
fy = 1607.7
cx = 655.3
cy = 414.4

# Defining the camera matrix K
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]])

t_x = 0
t_y = 0
t_z = 0.75
ang_x = 90 
ang_y = 0 
ang_z = 180

def load_csv_data(csv_file_path):
    """Load object data from a CSV file."""
    data = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def clear_cameras():
    """Remove all camera objects from the scene."""
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            bpy.data.objects.remove(obj, do_unlink=True)

def clear_lights():
    """Remove all light objects from the scene."""
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

def clear_scene_of_cars():
    """Remove all car objects from the scene."""
    for obj in bpy.data.objects:
        if "Car" in obj.name:  # Adjust if your car objects are named differently
            bpy.data.objects.remove(obj, do_unlink=True)

def render_scene():
    """Render the current frame and display it in the viewport."""
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
    bpy.ops.render.render('INVOKE_DEFAULT')

def clear_all_objects():
    """Remove all objects from the scene."""
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

def setup_light():
    """Create a light source and place it higher in the scene."""
    light_data = bpy.data.lights.new(name="SceneLight", type='POINT')
    light_data.energy = 10  # Adjust the energy as needed
    light_obj = bpy.data.objects.new(name="SceneLight", object_data=light_data)
    light_obj.location = (0, 0, 40)  # Place the light 10 units high
    bpy.context.collection.objects.link(light_obj)

def setup_sun_light():
    """Create a sun light source and place it in the scene."""
    sun_data = bpy.data.lights.new(name="SceneSun", type='SUN')
    sun_data.energy = 1  # Sun light is very intense; adjust as needed
    sun_obj = bpy.data.objects.new(name="SceneSun", object_data=sun_data)
    sun_obj.location = (0, 0, 40)  # Sun location does not affect lighting
    sun_obj.rotation_euler = (math.radians(-45), 0, 0)  # Adjust angle as needed
    bpy.context.collection.objects.link(sun_obj)

def render_and_save_frame(frame_index, output_folder):
    """Render the current frame and save it to the output folder."""
    # Set the file path for the rendered image
    print("step 1")
    render_path = os.path.join(output_folder, f"frame_{frame_index:04d}.png")
    print("step 2")
    bpy.context.scene.render.filepath = render_path
    print("step 3")
    # Render the frame
    bpy.ops.render.render(write_still=True)
    
    # Confirm the render and save was successful
    print(f"Saved rendered frame {frame_index:04d} to {render_path}")

def get_cam_extrinsics():
    # Rotation matrices for each axis
    R_x = np.array([[1, 0, 0],
                    [0, math.cos(ang_x), -math.sin(ang_x)],
                    [0, math.sin(ang_x), math.cos(ang_x)]])

    R_y = np.array([[math.cos(ang_y), 0, math.sin(ang_y)],
                    [0, 1, 0],
                    [-math.sin(ang_y), 0, math.cos(ang_y)]])

    R_z = np.array([[math.cos(ang_z), -math.sin(ang_z), 0],
                    [math.sin(ang_z), math.cos(ang_z), 0],
                    [0, 0, 1]])

    # Combined rotation matrix
    R = np.dot(R_z, np.dot(R_y, R_x))

    T = (t_x, t_y, t_z)
    # T = np.array([[t_x], [t_y], [t_z]])

    return R, T

def setup_camera(t_x, t_y, t_z, ang_x, ang_y, ang_z):
    # Create a new camera data-block
    cam_data = bpy.data.cameras.new(name="SceneCamera")
    cam_data.lens = 15  # Example focal length in mm

    # Create a new object with the camera data-block
    cam_obj = bpy.data.objects.new(name="SceneCamera", object_data=cam_data)





    cam_obj.location = (t_x, t_y, t_z)
    cam_obj.rotation_mode = 'XYZ'
    cam_obj.rotation_euler = (math.radians(ang_x), math.radians(ang_y), math.radians(ang_z)) 


    # cam_obj.rotation_euler = (0, math.radians(180), 0)  

    # Link the camera object to the scene's collection
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj  # Set the active camera

    # Adjust other camera parameters as needed
    cam_data.clip_start = 0.01
    cam_data.clip_end = 100000.0



def car_coords_to_blender_location_rotation(row, R, T, image_width, image_height):
    """Calculate Blender world coordinates and rotation from CSV row data."""
    x1, y1, x2, y2 = float(row['bbox_x1']), float(row['bbox_y1']), float(row['bbox_x2']), float(row['bbox_y2'])
    depth = float(row['average_depth'])
    label = row['object_type']




    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    # Camera matrix inversion
    K_inv = np.linalg.inv(K)

    # Convert image coordinates to camera coordinates
    u, v = (x1 + x2) / 2, (y1 + y2) / 2
    
    
    
    Z=(1/depth)*1000
    X=((u-cx)*Z)/fx
    Y=((v-cy)*Z)/fy
    
    camera_coords=np.array([X,Y,Z])   




    # Transform to world coordinates
    P_world = np.dot(R.T, camera_coords-T)


    
    if label == "car" or label=="truck" or label=="person" or label=="motorcycle":
        location=(
            P_world[0],
            (-P_world[1])/2.5, 
            0
            )
    if label=="traffic light":
        location=(
            P_world[0],
            (-P_world[1])/2.5, 
            3.0
            )
            
    
    


    if label == "car" or label=="truck":
#        if float(row['angle']) <-30 and float(row['angle']) >-150:
#            rotation = (0, 0,0)
        if float(row['angle'])==0:
            rotation = (0, 0,0)
#        elif float(row['angle'])>30 and float(row['angle'])<150:
#            rotation = (0, 0,math.radians(180))
        else:
            rotation = (0, 0,math.radians(90+float(row['angle'])))
        
        if label=="truck":
            yaw=rotation[2]
            rotation=(0,0,yaw+math.pi)
    elif label == "traffic light":
        rotation = (math.radians(90),0,math.radians(90))
    elif label == "person":
        rotation = (math.radians(90),0,math.radians(180))
    elif label == "stop sign":
        rotation = (math.radians(90),0,math.radians(90))
    elif label == "motorcycle":
        rotation = (math.radians(90),0,math.radians(-90))


    return location, rotation

def append_and_place_object(blend_file_path, csv_obj_name, location, rotation,scale_factor):
    """Append an object from a .blend file and place it in the scene."""

    if csv_obj_name == "car":
        obj_name = "Car"
    elif csv_obj_name == "traffic light":
        obj_name = "Traffic_signal1"
    elif csv_obj_name == "person":
        obj_name = "BaseMesh_Man_Simple"
    elif csv_obj_name == "stop sign":
        obj_name = "StopSign_Geo"
    elif csv_obj_name == "truck":
        obj_name = "Truck"
    elif csv_obj_name == "motorcycle":
        obj_name = "B_Wheel"
    
        
    if csv_obj_name == "car":
        scale_factor=scale_factor
    elif csv_obj_name == "truck":
        scale_factor=scale_factor*0.05
    elif csv_obj_name == "person":
        scale_factor*=(0.07/0.12)
    elif csv_obj_name == "motorcycle":
        scale_factor*=10
    elif csv_obj_name == "traffic light":
        scale_factor*=10
    
        
    
    
    

    with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
        # Append only the object that matches obj_name
        if obj_name in data_from.objects:
            data_to.objects = [obj_name]
        else:
            # You could add more sophisticated mapping here if needed
            print(f"Object named '{obj_name}' not found in {blend_file_path}.")
            return

    # Add the object to the current scene's collection and set its location and rotation
    if data_to.objects:
        obj = data_to.objects[0]  # We expect a list with one object, the one we appended
        bpy.context.collection.objects.link(obj)
        obj.location = location
        obj.rotation_euler = rotation
        obj.scale=[scale_factor, scale_factor, scale_factor]


    


def recreate_scene(csv_file_path, blend_files, image_width, image_height, R, T, scale_factor):
    """Recreate the road scene based on CSV data."""
    data = load_csv_data(csv_file_path)
    previous_frame_index = -1
    
    for row in data:
        current_frame_index = int(row['frame_index'])

        # Clear the previously spawned cars if the frame index has changed
#        if previous_frame_index != current_frame_index:
#            # render_and_save_frame(current_frame_index, output_folder = "/Users/mayankbansal/Desktop/CV/EV/output_test/")
#            # clear_scene_of_cars()
#            clear_all_objects()
#            setup_sun_light()
#            setup_camera(t_x, t_y, t_z, ang_x, ang_y, ang_z)
#            # render_scene()  # Render the scene before clearing
#            # time.sleep(1)  # Pause to view the scene
#            previous_frame_index = current_frame_index
            

        label = row['object_type']
        print(label)
        if label in blend_files:
            blend_file_path = blend_files[label]
            location, rotation = car_coords_to_blender_location_rotation(row, R, T, image_width, image_height)
            append_and_place_object(blend_file_path, label, location, rotation,scale_factor)
            
        
        
def draw_lanes(csv_file_lanes,R,T):
    """Draw lanes based on CSV data."""
    data = load_csv_data(csv_file_lanes)
    
    #combine all the points which  belong to the same lane and draw the lane as a bezier curve in blender
    lane_points={}
    for row in data:
        lane_num = int(row['lane_num'])
        if lane_num not in lane_points:
            lane_points[lane_num]=[]
        u,v,depth = float(row['u']), float(row['v']), float(row['depth'])




        fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
        # Camera matrix inversion
        K_inv = np.linalg.inv(K)

        
        
        
        Z=(1/depth)*1000
        X=((u-cx)*Z)/fx
        Y=((v-cy)*Z)/fy
        
        camera_coords=np.array([X,Y,Z])   




        # Transform to world coordinates
        P_world = np.dot(R.T, camera_coords-T)


        
        
        location=(
            P_world[0],
            (-P_world[1])/2.5, 
            0
            )
        lane_points[lane_num].append(location)

    for lane_num,points in lane_points.items():
        # Create a new curve data-block
        curve_data = bpy.data.curves.new(name=f"Lane{lane_num}", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.fill_mode = 'FULL'
        curve_data.bevel_depth = 0.05
        curve_data.bevel_resolution = 5

        # Create a new object with the curve data-block
        curve_obj = bpy.data.objects.new(name=f"Lane{lane_num}", object_data=curve_data)

        # Link the curve object to the scene's collection
        bpy.context.collection.objects.link(curve_obj)

        # Create a new spline and set its points
        spline = curve_data.splines.new('BEZIER')
        spline.bezier_points.add(len(points)-1)
        for i, point in enumerate(points):
            x, y, z = point
            spline.bezier_points[i].co = (x, y, z-0.05)
            spline.bezier_points[i].handle_left = (x-1, y, z-0.025)
            spline.bezier_points[i].handle_right = (x+1, y, z-0.025)

        # Adjust other curve parameters as needed
        curve_data.resolution_u = 2

    
    

blend_files = {
"car": "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/Assets/Vehicles/SedanAndHatchback.blend",
"traffic light": "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/Assets/TrafficSignal.blend",
"person": "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/Assets/Pedestrain.blend",
"stop sign": "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/Assets/StopSign.blend",
"truck": "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/Assets/Vehicles/Truck.blend",
"motorcycle": "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/Assets/Vehicles/Motorcycle.blend",
# Add more mappings as needed
}
image_width = 1024
image_height = 1024

# image_width = 1024
# image_height = 1024

scale_factor = 0.01  # Example scale factor, adjust as needed

# clear_scene_of_cars()
# clear_cameras()


R,T = get_cam_extrinsics()
    

        
#go through all the object csv files int the object_csv folder and all the lane csv files in the lane_csv folder and render the scene
list_of_files = os.listdir("/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/object_csv")
list_of_files.sort()

for idx,file in enumerate(list_of_files):
    clear_all_objects()
    setup_camera(t_x, t_y, t_z, ang_x, ang_y, ang_z)
    # clear_lights()
    setup_sun_light()   
    csv_file_path = '/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/object_csv/'+file
    recreate_scene(csv_file_path, blend_files, image_width, image_height, R, T, scale_factor)
    #corresponding lane csv file
    #if the object_frame0000.jpg the lane csv file will be lane_frame0000.csv
    csv_file_lanes = '/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/lane_csv/'+file.replace("object","lane")
    draw_lanes(csv_file_lanes,R,T)
    render_and_save_frame(idx, output_folder = "/home/venkatesh/Documents/WPI/Courses/CV/P3/EV/output_test/")



