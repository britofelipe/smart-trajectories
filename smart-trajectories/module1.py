import pandas as pd
import geopandas as gpd
import movingpandas as mpd
import matplotlib.pyplot as plt
import ast
import os
from datetime import datetime
from shapely.geometry import Point
from shapely.geometry import LineString
from shapely.ops import nearest_points
from PIL import Image

# Reads the trajectories from a text file and write the processed data into a CSV file 
def txt_to_csv(txt_filename, csv_filename):
    if not os.path.exists(txt_filename):
        print("Text file not found.")
        return
    
    with open(txt_filename, 'r') as f:
        lines = f.readlines()

    df_list = []
    for line in lines:
        parts = line.strip().split(', ')

        identifier = float(parts[0])
        category = float(parts[1])
        start_time = float(parts[2])
        end_time = float(parts[3])

        # Points array
        points_string = ', '.join(parts[4:])
        points = ast.literal_eval(points_string)

        time_interval = (end_time - start_time) / len(points)

        for i, point in enumerate(points):
            timestamp = start_time + i * time_interval
            x, y = point
            df_list.append([identifier, category, timestamp, x, y])

    df = pd.DataFrame(df_list, columns=['identifier', 'category', 'timestamp', 'x', 'y'])
    df.to_csv(csv_filename, index=False)

def txt_to_csv_datetime(txt_filename, csv_filename):
    if not os.path.exists(txt_filename):
        print("Text file not found.")
        return
    
    with open(txt_filename, 'r') as f:
        lines = f.readlines()

    df_list = []
    for line in lines:
        parts = line.strip().split(', ')

        identifier = int(parts[0])
        category = int(parts[1])
        start_time = datetime.strptime(parts[2], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(parts[3], "%Y-%m-%d %H:%M:%S.%f")

        # Points array
        points_string = ', '.join(parts[4:])
        points = ast.literal_eval(points_string)

        total_seconds = (end_time - start_time).total_seconds()
        time_interval = total_seconds / len(points)

        for i, point in enumerate(points):
            timestamp = (start_time + pd.Timedelta(seconds=i * time_interval)).timestamp()
            x, y = point
            df_list.append([identifier, category, timestamp, x, y])

    df = pd.DataFrame(df_list, columns=['identifier', 'category', 'timestamp', 'x', 'y'])
    df.to_csv(csv_filename, index=False)

# Transforms a CSV into a Trajectory Collection
def generate_trajectory_collection(filename):
    df = pd.read_csv(filename)

    # Transforms the column "Timestamp" into a datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Converts "x" and "y" into a Point column
    df['geometry'] = df.apply(lambda row: Point(row.x, row.y), axis=1)

    # Removes "x" and "y"
    df = df.drop(['x', 'y'], axis=1)

    # Creates a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = "EPSG:4326"

    # Defines timestamp as the index
    gdf.set_index('timestamp', inplace=True)

    # Creates an object objeto TrajectoryCollection
    traj_collection = mpd.TrajectoryCollection(gdf, 'identifier')

    return traj_collection

# Plot all trajectories
def plot_trajectories(traj_collection):
    plt.figure(figsize=(xsize, ysize))
    
    for traj in traj_collection:
        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]
        
        plt.plot(x_coords, y_coords, linewidth=linewidth, alpha=alpha)
    
    plt.xlim(xlim1, xlim2)  
    plt.ylim(ylim1, ylim2)  

    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Trajectories')
    plt.show()

# Plots by category
def plot_trajectories_categorized(traj_collection):
    plt.figure(figsize=(xsize, ysize))

    for traj in traj_collection:
        category = traj.df['category'].iloc[0]

        if category in category_colors:
            color = category_colors[category]
        else:
            color = 'gray'  

        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]
        
        plt.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha) 
    
    plt.xlim(xlim1, xlim2) 
    plt.ylim(ylim1, ylim2) 

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Trajectories')
    plt.show()

# Plots one category selected
def plot_trajectories_one_category(traj_collection, category):
    plt.figure(figsize=(xsize, ysize))

    if category not in category_colors:
        print("Category not recognized. Use a valid category.")
        return
    
    color = category_colors[category]

    for traj in traj_collection:
        traj_category = traj.df['category'].iloc[0]

        if traj_category != category:
            continue
        
        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]
        
        plt.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha)
    
    plt.xlim(xlim1, xlim2)
    plt.ylim(ylim1, ylim2)  

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Trajectories for category {category}')
    plt.show()

# Plot with an image of the location
def plot_trajectories_with_background(traj_collection, background_image_path):
    img = Image.open(background_image_path)

    plt.figure(figsize=(xsize, ysize))

    plt.imshow(img, extent=[min_x, max_x, max_y, min_y])

    for traj in traj_collection:
        category = traj.df['category'].iloc[0]

        if category in category_colors:
            color = category_colors[category]
        else:
            color = 'gray'  

        # Obtenha as coordenadas x e y de cada ponto na trajetória
        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]
        
        # Plote a trajetória
        plt.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha) 
    
    plt.xlim(xlim1, xlim2)  
    plt.ylim(ylim1, ylim2) 

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Trajectories')
    plt.show()

# Plot one category with background
def plot_trajectories_one_category_background(traj_collection, category, background_image_path):
    img = Image.open(background_image_path)

    plt.figure(figsize=(xsize, ysize))

    plt.imshow(img, extent=[min_x, max_x, max_y, min_y])

    color = category_colors[category]

    for traj in traj_collection:
        traj_category = traj.df['category'].iloc[0]

        if traj_category != category:
            continue
        
        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]
        
        plt.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha)
    
    plt.xlim(xlim1, xlim2)  
    plt.ylim(ylim1, ylim2) 

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Trajectories')
    plt.show()

def plot_trajectories_with_limits(traj_collection, category, background_image_path):
    img = Image.open(background_image_path)

    plt.figure(figsize=(xsize, ysize))

    plt.imshow(img, extent=[min_x, max_x, max_y, min_y])

    color = category_colors[category]

    # Draws the reference
    x_coords_line = [point[0] for point in reference_line.coords]
    y_coords_line = [point[1] for point in reference_line.coords]  

    plt.plot(x_coords_line, y_coords_line, color='red', linewidth=2)

    for traj in traj_collection:
        traj_category = traj.df['category'].iloc[0]

        if traj_category != category:
            continue

        line = LineString([(point.x, point.y) for point in traj.df.geometry])

        
        # Verifica se a trajetória passou a linha de referência
        if line.intersects(reference_line):
            intersections = line.intersection(reference_line)
            if intersections.geom_type == 'Point':
                intersection = intersections
            else:
                intersection = nearest_points(line, reference_line)[0]

            intersection_x = intersection.x
            intersection_y = intersection.y
            intersection_point = Point(intersection_x, intersection_y)

            closest_timestamp = None
            closest_distance = float('inf')

            for timestamp in traj.df.index:
                x, y = traj.df.loc[timestamp, 'geometry'].x, traj.df.loc[timestamp, 'geometry'].y
                point = Point(x, y)
                distance = point.distance(intersection_point)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_timestamp = timestamp

            print(f'Trajectory {traj.df["identifier"].iloc[0]} (Category: {traj.df["category"].iloc[0]}) crossed the reference line at {closest_timestamp}')

        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]

        plt.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha)
    
    plt.xlim(xlim1, xlim2)  
    plt.ylim(ylim1, ylim2) 

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Trajectories')
    plt.show()

def plot_trajectories_with_start_finish(traj_collection, category, background_image_path):
    img = Image.open(background_image_path)

    plt.figure(figsize=(xsize, ysize))

    plt.imshow(img, extent=[min_x, max_x, max_y, min_y])

    color = category_colors[category]

    # Draws the reference lines
    # Draws the reference lines
    for reference_line, line_color in [(arrival_line, 'red'), (departure_line, 'green')]:
        x_coords_line = [point[0] for point in reference_line.coords]
        y_coords_line = [point[1] for point in reference_line.coords]
        plt.plot(x_coords_line, y_coords_line, color=line_color, linewidth=4)

    for traj in traj_collection:
        traj_category = traj.df['category'].iloc[0]

        if traj_category != category:
            continue

        line = LineString([(point.x, point.y) for point in traj.df.geometry])

        # Initialize variable to store the state of whether the vehicle is going the wrong way
        wrong_way = False

        # Initialize the closest timestamps
        closest_timestamp_arrival = None
        closest_timestamp_departure = None

        # Check if the trajectory crossed arrival line first (indicating wrong way)
        if line.intersects(arrival_line):
            intersections = line.intersection(arrival_line)
            if intersections.geom_type == 'Point':
                intersection = intersections
            else:
                intersection = nearest_points(line, arrival_line)[0]

            intersection_x = intersection.x
            intersection_y = intersection.y
            intersection_point = Point(intersection_x, intersection_y)

            closest_distance_arrival = float('inf')

            for timestamp in traj.df.index:
                x, y = traj.df.loc[timestamp, 'geometry'].x, traj.df.loc[timestamp, 'geometry'].y
                point = Point(x, y)
                distance = point.distance(intersection_point)

                if distance < closest_distance_arrival:
                    closest_distance_arrival = distance
                    closest_timestamp_arrival = timestamp

        # Check if the trajectory crossed departure line
        if line.intersects(departure_line):
            intersections = line.intersection(departure_line)
            if intersections.geom_type == 'Point':
                intersection = intersections
            else:
                intersection = nearest_points(line, departure_line)[0]

            intersection_x = intersection.x
            intersection_y = intersection.y
            intersection_point = Point(intersection_x, intersection_y)

            closest_distance_departure = float('inf')

            for timestamp in traj.df.index:
                x, y = traj.df.loc[timestamp, 'geometry'].x, traj.df.loc[timestamp, 'geometry'].y
                point = Point(x, y)
                distance = point.distance(intersection_point)

                if distance < closest_distance_departure:
                    closest_distance_departure = distance
                    closest_timestamp_departure = timestamp

            # If the trajectory crossed the arrival line first, then it's going the wrong way
            if closest_timestamp_arrival is not None and closest_timestamp_departure > closest_timestamp_arrival:
                wrong_way = True
                print(f'Warning: Trajectory {traj.df["identifier"].iloc[0]} (Category: {traj.df["category"].iloc[0]}) is going the wrong way!')

            print(f'Trajectory {traj.df["identifier"].iloc[0]} (Category: {traj.df["category"].iloc[0]}) crossed the departure line at {closest_timestamp_departure}')

        x_coords = [point.x for point in traj.df.geometry]
        y_coords = [point.y for point in traj.df.geometry]

        if wrong_way:
            plt.plot(x_coords, y_coords, color='red', linewidth=linewidth, alpha=alpha)
        else:
            plt.plot(x_coords, y_coords, color=color, linewidth=linewidth, alpha=alpha)
    
    plt.xlim(xlim1, xlim2)  
    plt.ylim(ylim1, ylim2) 

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Trajectories')
    plt.show()


# Category colors
category_colors = {
    0.0: 'darkorange',
    1.0: 'blue',
    2.0: 'orange',
    3.0: 'darkgreen',
    4.0: 'olive',
    5.0: 'black',
}




# RUNNING 3
xlim1 = 50
xlim2 = 1800
ylim1 = 900
ylim2 = 0
xsize = 16
ysize = 8
min_x = 50
max_x = 1800
min_y = 0
max_y = 990

linewidth = 2
alpha = 0.35

# Loading data

txt_to_csv_datetime('assets/trail_points_data_2.txt', 'assets/trail_points_data_2.csv')

traj_collection = generate_trajectory_collection('assets/trail_points_data_2.csv')



# Simple plots

plot_trajectories_categorized(traj_collection)

plot_trajectories_with_background(traj_collection, './assets/background_2.jpg')

linewidth = 3
alpha = 0.7

plot_trajectories_one_category_background(traj_collection, 0.0, './assets/background_2.jpg')



# USING LIMITS

# Test 1

reference_y = 200
reference_x = 400

reference_line = LineString([(min_x, reference_y), (max_x, reference_y)])

plot_trajectories_with_limits(traj_collection, 1.0, './assets/background_2.jpg')


# Test 2

reference_y = 200
reference_x = 400

reference_line = LineString([(0, 500), (1000, 900)])

plot_trajectories_with_limits(traj_collection, 2.0, './assets/background_2.jpg')


# Test 3

reference_line = LineString([(0, 500), (1000, 900)])

plot_trajectories_with_limits(traj_collection, 3.0, './assets/background_2.jpg')


# Test 4

reference_line = LineString([(0, 500), (1000, 900)])

plot_trajectories_with_limits(traj_collection, 5.0, './assets/background_2.jpg')


# Test 5 - Pedestrians

reference_line = LineString([(400, 0), (1000, 900)])

plot_trajectories_with_limits(traj_collection, 0.0, './assets/background_2.jpg')


# USING TWO REFERENCE LINES

departure_line = LineString([(min_x, 100), (max_x, 100)])
arrival_line = LineString([(min_x, 500), (max_x, 500)])

plot_trajectories_with_start_finish(traj_collection, 1.0, './assets/background_2.jpg')

departure_line = LineString([(min_x, 150), (max_x, 150)])
arrival_line = LineString([(min_x, 300), (max_x, 300)])

plot_trajectories_with_start_finish(traj_collection, 2.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 3.0, './assets/background_2.jpg')


# Testing shorter paths

departure_line = LineString([(min_x, 100), (620, 100)])
arrival_line = LineString([(min_x, 500), (1000, 500)])

plot_trajectories_with_start_finish(traj_collection, 1.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 2.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 3.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 4.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 5.0, './assets/background_2.jpg')

# Curious case

arrival_line = LineString([(min_x, 500), (max_x, 500)])
plot_trajectories_with_start_finish(traj_collection, 1.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 2.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 3.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 4.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 5.0, './assets/background_2.jpg')


# Testing shorter paths 2

arrival_line = LineString([(550, 100), (max_x, 100)])
departure_line = LineString([(1000, 500), (max_x, 500)])

plot_trajectories_with_start_finish(traj_collection, 1.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 2.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 3.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 4.0, './assets/background_2.jpg')
plot_trajectories_with_start_finish(traj_collection, 5.0, './assets/background_2.jpg')

# Curious case

departure_line = LineString([(min_x, 500), (max_x, 500)])
plot_trajectories_with_start_finish(traj_collection, 5.0, './assets/background_2.jpg')