import pandas as pd
from multiprocessing import Pool, cpu_count


def match_data(args):
    trajectory_data, bus_stops_buffer, bus_stops_buffer_extended = args
    for i in range(len(trajectory_data)):
        for stop in range(len(bus_stops_buffer)):
            if bus_stops_buffer.iloc[stop].geometry.contains(trajectory_data.iloc[i].geometry):
                trajectory_data.at[i, 'bus_stop'] = bus_stops_buffer.at[stop, 'stop_id']
                break
            elif bus_stops_buffer_extended.iloc[stop].geometry.contains(trajectory_data.iloc[i].geometry):
                trajectory_data.at[i, 'bus_stop'] = bus_stops_buffer_extended.at[stop, 'stop_id']
                break
    return trajectory_data


def match_gps_data_with_bus_stops(trajectory_data, bus_stops_buffer, bus_stops_buffer_extended):
    num_processes = cpu_count() - 1  # Number of available CPU coresq
    chunk_size = len(trajectory_data) // num_processes
    chunks = [(trajectory_data[i:i + chunk_size], bus_stops_buffer, bus_stops_buffer_extended)
              for i in range(0, len(trajectory_data), chunk_size)]
    with Pool(processes=num_processes) as pool:
        updated_chunks = pool.map(match_data, chunks)
    return pd.concat(updated_chunks, ignore_index=True)

def match_bus_stops(bus_trajectory, bus_stops_buffer1, bus_stops_buffer2, bus_stops_buffer1_extended,
                    bus_stops_buffer2_extended):
    """

      Filter bus trip data of two buffer ranges with all the bus points, only bus stops points.

      Args:
          bus_trajectory (pd.DataFrame): Sequence of bus trip trajectory data
          bus_stops_buffer1 (GeoDataFrame) : Buffer created for filtered  Kandy-Digana direction.
          bus_stops_buffer2 (GeoDataFrame) : Buffer created for filtered  Digana-Kandy direction
          bus_stops_buffer1_extended (GeoDataFrame) : Additional buffer created for filtered  Kandy-Digana direction.
          bus_stops_buffer2_extended (GeoDataFrame) : Additional buffer created for filtered  Digana-Kandy direction.

      Returns:
          bus_trip_all_points (pd.DataFrame): Bus trip data with all points including null for bus_stop
          bus_stop_all_points (pd.DataFrame): Bus trip data with only bus_stops points

    """

    # project to local coordinate system before buffer filtering
    bus_trajectory = bus_trajectory.to_crs('EPSG:5234')
    # split trajectories by direction
    trajectory_dir_1 = bus_trajectory[bus_trajectory['direction'] == 1]
    trajectory_dir_2 = bus_trajectory[bus_trajectory['direction'] == 2]
    # reset index before for loop
    trajectory_dir_1.reset_index(drop=True, inplace=True)
    trajectory_dir_2.reset_index(drop=True, inplace=True)
    # filter records within bus stops buffer of both directions
    trajectory_dir_1 = match_gps_data_with_bus_stops(trajectory_dir_1, bus_stops_buffer1, bus_stops_buffer1_extended)

    trajectory_dir_2 = match_gps_data_with_bus_stops(trajectory_dir_2, bus_stops_buffer2, bus_stops_buffer2_extended)

    # concatenate dataframes of both directions and keep only records filtered within bus stops
    bus_trip_all_points = pd.concat([trajectory_dir_1, trajectory_dir_2])
    bus_stop_all_points = bus_trip_all_points.dropna()

    return bus_trip_all_points, bus_stop_all_points
