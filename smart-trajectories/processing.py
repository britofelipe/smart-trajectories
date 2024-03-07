import pandas as pd
import movingpandas as mpd
import geopandas as gpd
from shapely.geometry import Point

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