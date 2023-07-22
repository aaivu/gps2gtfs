import pandas as pd
from datetime import datetime, date
import numpy as np


def find_end_time_and_end_terminals(bus_trips):
    bus_trips[['end_time', 'end_terminal']] = bus_trips[['time', 'bus_stop']].shift(-1)
    return bus_trips.iloc[::2]


def find_direction(bus_trips):
    conditions = [(bus_trips['start_terminal'] == 'BT01'),
                  (bus_trips['start_terminal'] == 'BT02')]
    values = [1, 2]

    return np.select(conditions, values)


def calculate_trip_duration(bus_trips):
    bus_trips['duration'] = pd.Series(dtype='object')
    for i in range(len(bus_trips)):
        bus_trips.at[i, 'duration'] = datetime.combine(date.min, bus_trips.at[i, 'end_time']) - datetime.combine(
            date.min, bus_trips.at[i, 'start_time'])

    bus_trips['duration_in_mins'] = bus_trips['duration'] / np.timedelta64(1, 'm')
    return bus_trips


def trip_data_extraction(trip_ends):
    """
      To extract bus trips with derived columns.
      Create end_time, end_terminal for a bus trip.
      Create features of duration, duration_in_mins, day_of_the_week, hour_of_day

      Args:
          trip_ends (pd.DataFrame): Filtered bus trip data with terminals.

      Returns:
          bus_trips (pd.DataFrame): Bus trip terminals data with derived features.
    """

    bus_trips = trip_ends.copy()
    bus_trips = find_end_time_and_end_terminals(bus_trips)

    bus_trips = bus_trips.drop(
        ['id', 'devicetime', 'latitude', 'longitude', 'speed', 'geometry', 'grouped_ends', 'entry/exit'], axis=1)

    bus_trips.insert(0, 'trip_id', bus_trips.pop('trip_id'))
    bus_trips.rename(columns={'time': 'start_time', 'bus_stop': 'start_terminal'}, inplace=True)

    bus_trips['direction'] = find_direction(bus_trips)

    bus_trips = bus_trips[
        ['trip_id', 'deviceid', 'date', 'start_terminal', 'end_terminal', 'direction', 'start_time', 'end_time']]
    bus_trips = bus_trips.reset_index(drop=True)

    # Calculate trip duration
    bus_trips = calculate_trip_duration(bus_trips)

    bus_trips['day_of_week'] = pd.to_datetime(bus_trips['date']).dt.weekday
    bus_trips['hour_of_day'] = list(map(lambda x: x.hour, (bus_trips['start_time'])))

    return bus_trips
