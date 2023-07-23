import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def dwell_time_calculation(bus_stop_all_points):
    """
      Drop terminal points from all points data.
      Calculate arrival_time, departure_time according to check whether grouped record has 0 speed values or not.
      Dwell time derived in seconds.

      Args:
          bus_stop_all_points (pd.DataFrame): Bus trip data with only bus_stops points

      Returns:
          bus_stop_times (pd.DataFrame): Bus stops data with arrival_time, departure_time, dwell_time for each stops excluding terminals.

     """

    # Drop records with End Bus terminals
    bus_stop_all_points.drop(bus_stop_all_points[bus_stop_all_points['bus_stop'] == 'BT01'].index, inplace=True)
    bus_stop_all_points.drop(bus_stop_all_points[bus_stop_all_points['bus_stop'] == 'BT02'].index, inplace=True)

    # grouping all records filtered for every bus stop
    bus_stop_all_points['grouped_ends'] = (
        (bus_stop_all_points['bus_stop'].shift() != bus_stop_all_points['bus_stop'])).cumsum()

    # creating a new dataframe for bus stop times
    columns = ['trip_id', 'deviceid', 'date', 'direction', 'bus_stop', 'arrival_time', 'departure_time', 'dwell_time']
    bus_stop_times = pd.DataFrame(columns=columns)

    # Loop over every grouped filtered records and choose the two records that indicate bus arrival and departure to the stop
    for name, group in bus_stop_all_points.groupby('grouped_ends'):
        if 0 in group[
            'speed'].values:  # if the grouped filter record has '0" speed values, then bus has stopped more than 15 seconds there and first '0'speed record as the arrival
            values = []
            trip_id = np.unique(group['trip_id'].values)[0]
            direction = np.unique(group['direction'].values)[0]
            deviceid = np.unique(group['deviceid'].values)[0]
            date = np.unique(group['date'].values)[0]
            bus_stop = np.unique(group['bus_stop'].values)[0]

            arrival_time = group[group['speed'] == 0]['time'].min()

            buffer_leaving_time = group['time'].max()
            rough_departure_time = group[group['speed'] == 0]['time'].max()

            if (datetime.combine(date.min, buffer_leaving_time) - datetime.combine(date.min,
                                                                                   rough_departure_time)).total_seconds() > 15:
                departure_time = (datetime.combine(date.min, rough_departure_time) + timedelta(seconds=15)).time()
            else:
                departure_time = buffer_leaving_time

            values.extend([trip_id, deviceid, date, direction, bus_stop, arrival_time, departure_time])
            bus_stop_times = bus_stop_times.append(dict(zip(columns, values)), True)

        else:
            values = []
            trip_id = np.unique(group[['trip_id']].values)[0]
            direction = np.unique(group['direction'].values)[0]
            deviceid = np.unique(group[['deviceid']].values)[0]
            date = np.unique(group['date'].values)[0]
            bus_stop = np.unique(group['bus_stop'].values)[0]

            arrival_time = group['time'].min()
            departure_time = arrival_time

            values.extend([trip_id, deviceid, date, direction, bus_stop, arrival_time, departure_time])
            bus_stop_times = bus_stop_times.append(dict(zip(columns, values)), True)

    for i in range(len(bus_stop_times)):
        bus_stop_times.at[i, 'dwell_time'] = datetime.combine(date.min, bus_stop_times.at[
            i, 'departure_time']) - datetime.combine(date.min, bus_stop_times.at[i, 'arrival_time'])

    bus_stop_times['dwell_time_in_seconds'] = bus_stop_times['dwell_time'] / np.timedelta64(1, 's')

    return bus_stop_times


def dwell_time_feature_addition(bus_stop_times):
    """
      To created additional derieved features for bus stops data.

      Args:
          bus_stop_times (pd.DataFrame): Bus stops data with arrival_time, departure_time, dwell_time for each stops excluding terminals.

      Returns:
          bus_stop_times (pd.DataFrame): Bus stops data with created features.

    """

    # bus_stop_times = bus_stop_times.drop(bus_stop_times[bus_stop_times['dwell_time_in_seconds']>threshold].index )

    bus_stop_times['day_of_week'] = pd.to_datetime(bus_stop_times['date']).dt.weekday
    bus_stop_times['hour_of_day'] = list(map(lambda x: x.hour, (bus_stop_times['arrival_time'])))
    bus_stop_times['weekday/end'] = list(map(lambda x: 1 if x < 5 else 0, (bus_stop_times['day_of_week'])))

    return bus_stop_times
