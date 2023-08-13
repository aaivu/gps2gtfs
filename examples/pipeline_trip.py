from gps2gtfs.pipeline.trip import run


if __name__ == "__main__":
    raw_gps_data_path = "./raw_data/digana_2022_07.csv"
    trip_terminals_data_path = "./raw_data/bus_terminals_654.csv"
    terminals_buffer_radius = 100

    run(
        raw_gps_data_path,
        trip_terminals_data_path,
        terminals_buffer_radius,
    )
