import pandas as pd
import geopandas as gpd
from ..utility import geo_data_frame_utility
from datetime import datetime, date


def bus_stop_buffer_create(gps_data, bus_stops, stop_buffer, extra_buffer):
    """

      Buffer and additional buffer  created  to accomodate points if they were missed in standard stop buffer.

      Args:
          gps_data (pd.DataFrame): Cleaned gps data filtered out from the server for the required time window.
          bus_stops (pd.DataFrame) : Bus stops data for the trip route
          stop_buffer (int):  Radius of the buffer area to represent bus stops
          extra_buffer (int):  Extended radius of the buffer area to represent bus stops.

      Returns:
          bus_stops_buffer1 (GeoDataFrame) : Buffer created for filtered  Kandy-Digana direction.
          bus_stops_buffer2 (GeoDataFrame) : Buffer created for filtered  Digana-Kandy direction
          gps_data (GeoDataFrame) :  GPS data as GeoDataFrame with projected corrdinates.
          bus_stops_buffer1_extended (GeoDataFrame) : Additional buffer created for filtered  Kandy-Digana direction.
          bus_stops_buffer2_extended (GeoDataFrame) : Additional buffer created for filtered  Digana-Kandy direction.
    """

    gps_data = geo_data_frame_utility.convert_to_geo_data_frame(gps_data)
    bus_stops = geo_data_frame_utility.convert_to_geo_data_frame(bus_stops)
    # split bus stops dataframe into two based on route direction
    bus_stops_direction1 = bus_stops[bus_stops['direction'] == 'Kandy-Digana']
    bus_stops_direction2 = bus_stops[bus_stops['direction'] == 'Digana-Kandy']

    bus_stops_direction2.reset_index(drop=True, inplace=True)

    # proximity analysis
    # creating a buffer
    bus_stops_buffer1 = geo_data_frame_utility.geo_buffer_extend(bus_stops_direction1, stop_buffer)
    bus_stops_buffer2 = geo_data_frame_utility.geo_buffer_extend(bus_stops_direction2, stop_buffer)

    # creating additional extra buffer to accommodate points if they were missed in standard stop buffer
    bus_stops_buffer1_extended = geo_data_frame_utility.geo_buffer_extend(bus_stops_direction1, extra_buffer)
    bus_stops_buffer2_extended = geo_data_frame_utility.geo_buffer_extend(bus_stops_direction2, extra_buffer)

    return bus_stops_buffer1, bus_stops_buffer2, gps_data, bus_stops_buffer1_extended, bus_stops_buffer2_extended


def prepare_bus_trajectory_data(gps_data, processed_data, bus_trips):
    """
      Create bus trajectory data of sequence of bus stops with direction of trip.

      Args:
          gps_data (GeoDataFrame): Bus trips GPS data
          processed_data (pd.DataFrame) : Split trip data from bus_trip_extraction.py
          bus_trips (pd.DataFrame) : Bus trips data

      Returns:
          bus_trajectory (pd.DataFrame): Sequence of bus trip trajectory data
    """

    # gps records that are matched with end terminals, are merged with whole GPS records
    processed_data = processed_data[['id', 'bus_stop', 'trip_id']]
    bus_trajectory = pd.merge(left=gps_data, right=processed_data, how='outer', left_on='id', right_on='id')

    # gps records that are not associated with the terminals are asssigned as trip id = 0
    bus_trajectory["trip_id"].fillna(0, inplace=True)

    # run a loop to assign trip_id to records that are in between the terminals
    bus_trajectory.reset_index(drop=True, inplace=True)

    trip = 1
    for i in range(len(bus_trajectory) - 1):
        if bus_trajectory.at[i, 'trip_id'] == trip:
            if bus_trajectory.at[i + 1, 'trip_id'] == 0:
                bus_trajectory.at[i + 1, 'trip_id'] = trip
            elif bus_trajectory.at[i + 1, 'trip_id'] == trip:
                trip = trip + 1

    bus_trajectory.drop(bus_trajectory[bus_trajectory['trip_id'] == 0].index,
                        inplace=True)  # drop records that are not identified as a bus trip

    # Identify the directions of each bus trajectories using bus trips extracted data
    directions = bus_trips.set_index('trip_id').to_dict()['direction']
    bus_trajectory['direction'] = list(map(lambda x: directions[x], bus_trajectory['trip_id']))

    return bus_trajectory
