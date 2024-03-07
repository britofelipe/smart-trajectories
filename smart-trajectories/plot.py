import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.ops import nearest_points
from PIL import Image
from shapely.geometry import LineString

# Category colors
category_colors_template = {
    0.0: 'darkorange',
    1.0: 'blue',
    2.0: 'orange',
    3.0: 'darkgreen',
    4.0: 'olive',
    5.0: 'black',
}

# Plot all trajectories
def plot_trajectories(traj_collection, xsize, ysize, xlim1, xlim2, ylim1, ylim2, linewidth=2, alpha=0.35):
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
def plot_trajectories_categorized(traj_collection, xsize, ysize, xlim1, xlim2, ylim1, ylim2, linewidth=2, alpha=0.35, category_colors=category_colors_template):
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
def plot_trajectories_one_category(traj_collection, category, xsize, ysize, xlim1, xlim2, ylim1, ylim2, linewidth=2, alpha=0.35, category_colors=category_colors_template):
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
def plot_trajectories_with_background(traj_collection, background_image_path, xsize, ysize, xlim1, xlim2, ylim1, ylim2, min_x, max_x, min_y, max_y, category_colors=category_colors_template, linewidth=2, alpha=0.35):
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
def plot_trajectories_one_category_background(traj_collection, category, background_image_path,  xsize, ysize, xlim1, xlim2, ylim1, ylim2, min_x, max_x, min_y, max_y, category_colors=category_colors_template, linewidth=2, alpha=0.35):
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

def plot_trajectories_with_limits(traj_collection, category, background_image_path, reference_line, xsize, ysize, xlim1, xlim2, ylim1, ylim2, min_x, max_x, min_y, max_y, category_colors=category_colors_template, linewidth=2, alpha=0.35):
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

def plot_trajectories_with_start_finish(traj_collection, category, background_image_path, arrival_line, departure_line, xsize, ysize, xlim1, xlim2, ylim1, ylim2, min_x, max_x, min_y, max_y, category_colors=category_colors_template, linewidth=2, alpha=0.35):
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

