from gps2gfts.components.load_data import load_data_from_csv
from gps2gfts.components.pre_processing import data_cleaner
from gps2gfts.components.process_trip import extract_trips
from gps2gfts.components.process_trip import extract_trip_details
from datetime import datetime

if __name__ == '__main__':
    RAW_DATA_PATH = '../../raw_data/digana_2022_07.csv'
    BUS_TERMINALS_PATH = '../../raw_data/bus_terminals_654.csv'
    [read_raw_data, read_bus_terminals] = load_data_from_csv.read_data_from_path(RAW_DATA_PATH, BUS_TERMINALS_PATH)
    cleaned_gps_data = data_cleaner.raw_data_cleaning(read_raw_data)
    print(cleaned_gps_data)

    end_buffer = 100
    trip_ends = extract_trips.process_extract_trip(cleaned_gps_data, read_bus_terminals, end_buffer)
    bus_trips = extract_trip_details.trip_data_extraction(trip_ends)
    filename = "trip_ends" + '.csv'
    trip_ends.to_csv(filename, encoding='utf-8-sig', index=False)
    print(bus_trips)
    filename = "finn" + '.csv'
    bus_trips.to_csv(filename, encoding='utf-8-sig', index=False)
