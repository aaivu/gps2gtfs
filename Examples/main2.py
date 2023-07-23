from gps2gfts.components.load_data import load_data_from_csv
from gps2gfts.components.pre_processing import data_cleaner
from gps2gfts.components.process_bus_stops import prepare_bus_data
from gps2gfts.components.process_bus_stops import discover_bus_stop
from datetime import datetime

if __name__ == '__main__':
    RAW_DATA_PATH = '../../raw_data/digana_2022_07.csv'
    PATH_PROCESSED_DATA = 'trip_ends.csv'
    PATH_BUS_TRIPS = 'finn.csv'
    PATH_BUS_STOPS = '../../raw_data/bus_stops_654.csv'
    t1 = datetime.now()
    [read_raw_data, read_processed_data, read_bus_trips,
     read_bus_stops] = load_data_from_csv.read_data_for_bus_stop_calculation(RAW_DATA_PATH, PATH_PROCESSED_DATA,
                                                                             PATH_BUS_TRIPS, PATH_BUS_STOPS)
    print("time needed for read data")
    print(datetime.now()-t1)
    t1 = datetime.now()
    cleaned_gps_data = data_cleaner.raw_data_cleaning(read_raw_data)
    print("time needed for cleaning")
    print(datetime.now() - t1)
    t1 = datetime.now()
    stop_buffer = 50
    extra_buffer = 100
    bus_stops_buffer1, bus_stops_buffer2, gps_data, bus_stops_buffer1_extended, bus_stops_buffer2_extended = prepare_bus_data.bus_stop_buffer_create(
        cleaned_gps_data, read_bus_stops, stop_buffer, extra_buffer)
    print("time needed for bus buffer creation")
    print(datetime.now() - t1)
    t1 = datetime.now()
    bus_trajectory = prepare_bus_data.prepare_bus_trajectory_data(gps_data, read_processed_data, read_bus_trips)
    print("time needed for preparing trajectory data")
    print(datetime.now() - t1)
    t1 = datetime.now()
    result = discover_bus_stop.match_bus_stops(bus_trajectory, bus_stops_buffer1, bus_stops_buffer2,
                                               bus_stops_buffer1_extended,
                                               bus_stops_buffer2_extended)
    print("time needed for matching")
    print(datetime.now() - t1)
    filename = "abcd" + '.csv'
    result[1].to_csv(filename, encoding='utf-8-sig', index=False)
