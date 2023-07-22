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
