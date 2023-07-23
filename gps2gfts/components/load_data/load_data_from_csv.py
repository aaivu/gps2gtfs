import pandas as pd


def read_csv_file(path, type_of_data):
    try:
        # Attempt to read the CSV file
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"File not found error. Please check the file path for . Path provided is {path}")
    except pd.errors.ParserError:
        print(f"Parser error. The {type_of_data} file may have an invalid format.")
    except Exception as e:
        print(f"An unexpected error occurred when reading {type_of_data}. Error is {str(e)}")


def read_data_from_path(raw_data, bus_terminals_path):
    # reading RAW GPS Data
    read_raw_data = read_csv_file(raw_data, "raw GPS Data")
    # reading Bus Terminal Data
    read_bus_terminals = read_csv_file(bus_terminals_path, "Bus Terminal Data")
    return [read_raw_data, read_bus_terminals]


def read_data_for_bus_stop_calculation(raw_data_path, processed_gps_data_path, bus_trips_path, bus_stops_path):
    # reading RAW GPS Data
    read_raw_data = read_csv_file(raw_data_path, "raw GPS Data")
    # Processed Trip End
    read_processed_gps_data = read_csv_file(processed_gps_data_path, "Processed GPS Data")
    # Bus Trips
    read_bus_trips = read_csv_file(bus_trips_path, "Processed Bus Trips")
    # Bus Stops
    read_bus_stops = read_csv_file(bus_stops_path, "Processed Bus Stops")
    return [read_raw_data, read_processed_gps_data, read_bus_trips, read_bus_stops]
