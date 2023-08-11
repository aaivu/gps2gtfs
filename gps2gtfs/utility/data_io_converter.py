from typing import Optional

from geopandas import GeoDataFrame, points_from_xy
from pandas import DataFrame, errors, read_csv
from gps2gtfs.data_field.input_field import RawGPSField


def read_csv_file(path: str, file_name: str = None) -> Optional[DataFrame]:
    """
    Reads a CSV file and returns its content as a pandas DataFrame.

    Parameters:
        path (str): The file path of the CSV file to read.
        file_name (str, optional): The name of the CSV file. It is used for error reporting.
                                   Default is None.

    Returns:
        Optional[DataFrame]: A pandas DataFrame containing the content of the CSV file.
                             If the file is not found or there is an error while reading
                             the file, None is returned.

    Notes:
        - The function uses pandas' read_csv() function to read the CSV file.
        - If the file is not found, an error message is printed to the console.
        - If there is a parsing error, an error message is printed, indicating the
          potentially invalid format in the file.
        - For other unexpected errors, an error message is printed along with the
          specific error details.

    Example:
        >>> df = read_csv_file("data.csv")
        >>> if df is not None:
        ...     print(df.head())
        ... else:
        ...     print("Error occurred while reading the CSV file.")
    """
    try:
        return read_csv(path)
    except FileNotFoundError:
        print(
            f"File is not found. Please check the file path. Provided path is {path}."
        )
    except errors.ParserError:
        print(f"Parser error. The file {file_name} may has an invalid format.")
    except Exception as e:
        print(
            f"An unexpected error occurred when reading the file {file_name}. Error is {str(e)}"
        )


def write_as_csv_file(pd_df: DataFrame, path: str) -> None:
    """
    Write a pandas DataFrame to a CSV file.

    The function takes a pandas DataFrame and writes its contents to a CSV file specified by the
    provided file path. The function does not include the DataFrame index in the output CSV.

    Parameters:
        pd_df (DataFrame): The pandas DataFrame to be written to the CSV file.
        path (str): The file path where the CSV file will be saved.

    Returns:
        None

    Example:
        >>> import pandas as pd

        >>> data = {
        ...     'Name': ['John', 'Alice', 'Bob'],
        ...     'Age': [25, 30, 22],
        ...     'City': ['New York', 'San Francisco', 'Los Angeles']
        ... }
        >>> pd_df = pd.DataFrame(data)
        >>> file_path = "output.csv"
        >>> write_as_csv_file(pd_df, file_path)
        >>> print(f"Data written to {file_path}.")
    """
    pd_df.to_csv(path, index=False)


def pandas_to_geo_data_frame(raw_gps_pd_df: DataFrame) -> GeoDataFrame:
    """
    Convert a pandas DataFrame with raw GPS coordinates to a GeoDataFrame with points.

    The function takes a pandas DataFrame containing raw GPS coordinates (latitude and longitude)
    and converts it to a GeoDataFrame with points. It assumes that the DataFrame includes two
    columns named 'longitude' and 'latitude', which represent the longitude and latitude values,
    respectively.

    Parameters:
        raw_gps_pd_df (DataFrame): A pandas DataFrame containing raw GPS coordinates.

    Returns:
        GeoDataFrame: A geopandas GeoDataFrame containing points created from the provided
                      raw GPS coordinates.

    Notes:
        - The function uses the geopandas `GeoDataFrame` class and the `points_from_xy` function
          to create the GeoDataFrame with points.
        - The function sets the coordinate reference system (CRS) of the GeoDataFrame to EPSG:4326,
          which is the standard WGS 84 geographic coordinate system (latitude and longitude).
        - The resulting GeoDataFrame is then reprojected to EPSG:5234, which represents a different
          coordinate system (you can customize this according to your specific needs).

    Example:
        >>> import pandas as pd
        >>> from shapely.geometry import Point
        >>> from geopandas import GeoDataFrame

        >>> data = {
        ...     'longitude': [-73.9857, -122.4194, -118.2437],
        ...     'latitude': [40.7486, 37.7749, 34.0522]
        ... }
        >>> raw_gps_pd_df = pd.DataFrame(data)
        >>> geo_df = pandas_to_geo_data_frame(raw_gps_pd_df)
        >>> print(geo_df)
                           geometry
        0  POINT (40.7486 -73.9857)
        1  POINT (37.7749 -122.4194)
        2  POINT (34.0522 -118.2437)
    """
    geo_df = GeoDataFrame(
        data=raw_gps_pd_df,
        geometry=points_from_xy(
            raw_gps_pd_df[RawGPSField.LONGITUDE.value],
            raw_gps_pd_df[RawGPSField.LATITUDE.value],
        ),
        crs="EPSG:4326",
    )

    return geo_df.to_crs("EPSG:5234")


def extend_geo_buffer(geo_df: GeoDataFrame, distance: int) -> GeoDataFrame:
    """
    Extend the buffer of geometries in a GeoDataFrame.

    The function takes a geopandas GeoDataFrame and extends the buffer of its geometries by the
    specified distance. The distance determines how much each geometry's buffer will be increased.

    Parameters:
        geo_df (GeoDataFrame): A geopandas GeoDataFrame containing geometries.
        distance (int): The distance (in the coordinate system's units) by which to extend
                        the buffer of each geometry.

    Returns:
        GeoDataFrame: A new geopandas GeoDataFrame with the extended buffer geometries.

    Notes:
        - The function uses the `buffer` method of Shapely geometries to extend the buffer.
        - The buffer distance can be positive or negative. Positive values will expand the buffer,
          while negative values will shrink it.
        - The resulting GeoDataFrame will have geometries of the same type as the original.
        - The coordinate system of the resulting GeoDataFrame remains the same as the input.

    Example:
        >>> from geopandas import GeoDataFrame
        >>> from shapely.geometry import Point, LineString

        >>> data = {
        ...     'geometry': [Point(0, 0), LineString([(1, 1), (2, 2)])]
        ... }
        >>> geo_df = GeoDataFrame(data)
        >>> distance = 1
        >>> extended_geo_df = extend_geo_buffer(geo_df, distance)
        >>> print(extended_geo_df)
                                       geometry
        0      POLYGON ((-1 -1, -1 1, 1 1, 1 -1, -1 -1))
        1  LINESTRING (0 0, -0.7071067811865476 0.7071067811865476, -1 1, -1.707106781186547 1.707106781186547, -2 2)
    """
    return GeoDataFrame(
        data=geo_df,
        geometry=geo_df.geometry.buffer(distance),
    )
