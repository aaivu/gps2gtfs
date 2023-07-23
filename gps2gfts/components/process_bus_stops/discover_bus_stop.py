import pandas as pd


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
    print("erge")
    # split trajectories by direction
    trajectory_dir_1 = bus_trajectory[bus_trajectory['direction'] == 1]
    trajectory_dir_2 = bus_trajectory[bus_trajectory['direction'] == 2]
    print("ded")
    # reset index before for loop
    trajectory_dir_1.reset_index(drop=True, inplace=True)
    trajectory_dir_2.reset_index(drop=True, inplace=True)
    print("sfsf")
    # filter records within bus stops buffer of both directions
    for i in range(len(trajectory_dir_1)):
        if (i == 5000) : break
        for stop in range(len(bus_stops_buffer1)):
            if bus_stops_buffer1.iloc[stop].geometry.contains(trajectory_dir_1.iloc[i].geometry):
                trajectory_dir_1.at[i, 'bus_stop'] = bus_stops_buffer1.at[stop, 'stop_id']
            else:
                if bus_stops_buffer1_extended.iloc[stop].geometry.contains(trajectory_dir_1.iloc[i].geometry):
                    trajectory_dir_1.at[i, 'bus_stop'] = bus_stops_buffer1_extended.at[stop, 'stop_id']
    print("fd")
    for i in range(len(trajectory_dir_2)):
        if (i == 5000): break
        for stop in range(len(bus_stops_buffer2)):
            if bus_stops_buffer2.iloc[stop].geometry.contains(trajectory_dir_2.iloc[i].geometry):
                trajectory_dir_2.at[i, 'bus_stop'] = bus_stops_buffer2.at[stop, 'stop_id']
            else:
                if bus_stops_buffer2_extended.iloc[stop].geometry.contains(trajectory_dir_2.iloc[i].geometry):
                    trajectory_dir_2.at[i, 'bus_stop'] = bus_stops_buffer2_extended.at[stop, 'stop_id']

                    # concatenate dataframes of both directions and keep only records filtered within bus stops
    bus_trip_all_points = pd.concat([trajectory_dir_1, trajectory_dir_2])
    bus_stop_all_points = bus_trip_all_points.dropna()

    return bus_trip_all_points, bus_stop_all_points
