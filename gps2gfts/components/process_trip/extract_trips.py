import pandas as pd
import geopandas as gpd
from datetime import datetime
from multiprocessing import Pool, cpu_count


def convert_to_geo_data_frame(coordinate):
    # converting to GeoDataframe with Coordinate Reference system 4326
    coordinate = gpd.GeoDataFrame(coordinate, geometry=gpd.points_from_xy(coordinate.longitude, coordinate.latitude),
                                  crs='EPSG:4326')
    # project them in local coordinate system
    return coordinate.to_crs('EPSG:5234')


def match_gps_data_with_bus_terminals(args):
    gps_data, bus_terminals, end_buffer = args
    # creating buffer area to extract records around bus terminals
    bus_terminals_buffer = gpd.GeoDataFrame(bus_terminals, geometry=bus_terminals.geometry.buffer(end_buffer))
    # filtering coordinates within bus terminals end buffer
    gps_data['bus_stop'] = pd.Series(dtype='object')  # create a new column in gps data set
    gps_data.reset_index(drop=True, inplace=True)  # reset indices to run a for loop
    for i in range(len(gps_data)):
        for stop in range(len(bus_terminals)):
            if i > 200000: break
            if bus_terminals_buffer.iloc[stop].geometry.contains(gps_data.iloc[i].geometry):
                gps_data.at[i, 'bus_stop'] = bus_terminals.at[stop, 'terminal_id']
                break
    return gps_data


def extract_trip_ends(trip_ends):
    # grouping the filtered records of one bus terminal and one date
    trip_ends['grouped_ends'] = ((trip_ends['bus_stop'].shift() != trip_ends['bus_stop']) | (
            trip_ends['date'].shift() != trip_ends['date'])).cumsum()
    # find the entry or exit record only of the terminals
    # Early records is the entry(1) to the terminal and last record as the exit(0) to the end terminal
    trip_ends['entry/exit'] = pd.Series(dtype='object')
    trip_ends = trip_ends.reset_index(drop=True)

    # Find rows corresponding to maximum and minimum 'devicetime' in each group
    max_devicetime_rows = trip_ends.groupby('grouped_ends')['devicetime'].idxmax()
    min_devicetime_rows = trip_ends.groupby('grouped_ends')['devicetime'].idxmin()

    # Set 'entry/exit' column based on max and min 'devicetime' rows for each group
    trip_ends.loc[max_devicetime_rows, 'entry/exit'] = '0'
    trip_ends.loc[min_devicetime_rows, 'entry/exit'] = '1'
    # Drop rows with NaN values in 'entry/exit' column (if any)
    trip_ends.dropna(subset=['entry/exit'], inplace=True)
    return trip_ends.reset_index(drop=True)


def assign_trip_ids(trip_ends):
    trip = 0
    for i in range(len(trip_ends) - 1):
        if (trip_ends.at[i, 'bus_stop'] != trip_ends.at[i + 1, 'bus_stop']) & (
                trip_ends.at[i, 'date'] == trip_ends.at[i + 1, 'date']):
            trip = trip + 1
            trip_ends.at[i, 'trip_id'] = trip
            trip_ends.at[i + 1, 'trip_id'] = trip
    trip_ends = trip_ends.dropna()
    trip_ends = trip_ends.groupby('trip_id').filter(
        lambda x: len(x) > 1)  # remove outliers where no defined 2 trip ends for a trip
    return trip_ends


def process_extract_trip(gps_data, bus_terminals, end_buffer):
    """
      To extract trip ends dataframe with given buffer range.
      Filter the records within terminals selected buffer range.
      Within the filtered records get entry & exit to terminals.


      Args:
          gps_data (pd.DataFrame): Cleaned gps data filtered out from the server for the required time window.
          bus_terminals (pd.DataFrame): End and start terminals for the trip.
          end_buffer (int):  Radius of the buffer area to represent terminals.

      Returns:
          trip_ends (pd.DataFrame): Trip data with extracted terminals.
    """
    # converting to GeoDataframe
    gps_data = convert_to_geo_data_frame(gps_data)
    bus_terminals = convert_to_geo_data_frame(bus_terminals)
    # Split the GPS data into chunks to be processed in parallel
    num_processes = cpu_count()  # Number of available CPU coresq
    chunk_size = len(gps_data) // num_processes
    gps_data_chunks = [gps_data[i:i + chunk_size] for i in range(0, len(gps_data), chunk_size)]
    chunks = [(gps_data[i:i + chunk_size], bus_terminals, end_buffer)
              for i in range(0, len(gps_data), chunk_size)]
    with Pool(processes=num_processes) as pool:
        updated_chunks = pool.map(match_gps_data_with_bus_terminals, chunks)
    gps_data = pd.concat(updated_chunks, ignore_index=True)
    trip_ends = gps_data.dropna()  # filter records within terminal buffer
    # EXTRACT TRIP ENDS
    trip_ends = extract_trip_ends(trip_ends)
    # Providing unique trip id for trips which have entry / exit values within the 2 bus end terminals
    return assign_trip_ids(trip_ends)
