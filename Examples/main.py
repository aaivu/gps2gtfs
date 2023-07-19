from gps2gfts.components.load_data import load_data_from_csv

RAW_DATA_PATH = '../../raw_data/digana_2022_10.csv'
BUS_TERMINALS_PATH = '../../raw_data/bus_terminals_654.csv'
[read_raw_data, read_bus_terminals] = load_data_from_csv.read_data_from_path(RAW_DATA_PATH, BUS_TERMINALS_PATH)
print(read_raw_data)