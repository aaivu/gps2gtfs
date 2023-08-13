# gps2gtfs: A Python package to process raw GPS data of public transit and transform to GTFS format.

![project] ![research]

- <b>Project Lead(s) / Mentor(s)</b>

  1. Dr. T. Uthayasanker

- <b>Contributor(s)</b>
  1. R. Shiveswarran
  2. S. Gopinath
  3. S. Kajanan
  4. A. Kesavi

## Description

<div style="text-align:justify">

gps2gtfs is a python package that enables users to import for the task of preprocessing the GPS raw data and transfer to GTFS data. DataFrame and GeoDataFrame were used to handle data. Using new straight forward efficient techniques for raw GPS data to extract trips, stops sequence, dwell time at stops throughout the trip, travel time, running time in between stops and transfer to GTFS data. Currently the gps2gtfs package will handle static (schedule) heterogeneous traffic trip data, and in future can be implemented for dynamic real time trip data. Also the visualization package can be additionally combined with existing packages.

</div>
Keywords: GTFS, GPS, travel time, Public Transit, Heterogeneous traffic condition, ITS

## Architecture

<div style="text-align:justify">
gps2gtfs is written in Python 3. Package structure was implemented without coupling in between the packages. The main packages and functionalities are: data_field, load data, preprocessing, trip, stop, utility. Users should be given in- put only for one route. Multiple routes can be input to the pipeline using iteration by users.
</div>

The library is organized into six main modules:

- data_field will keep column names of user input and fixed number of output
  column names. Also fields of user input should be a super set of defined fields
  in this package.
- load_data to store trip and stop data for a route of a transit vehicle.
- preprocessing package will clean the above loaded data.
- stop package will identify stops and create stops related features.
- utility package has support utilities functions like io, conversions of data and loggers.
- pipeline package has the module to run trip and trip stop.

Architecture digram of gps2gfts
<img width="1000" alt="img1" src="https://github.com/aaivu/gps2gtfs/assets/74850246/678af0a8-64e3-49b5-8fb6-66b331ea7cae" >

<br>

How the gps2gfts works
<img width="1000" alt="img2" src="https://github.com/aaivu/gps2gtfs/assets/74850246/92cf2e62-2be4-49e1-b401-78ebbe20d194">

## Quick Example

The input files must be in CSV format. And a main thread should be there to use this package.

### 1. Pipeline to extract trips details

```python
from gps2gtfs.pipeline.trip import run


if __name__ == "__main__":
    raw_gps_data_path = "path/to/raw_gps_data/csv"
    trip_terminals_data_path = "path/to/trip_terminals_data/csv"
    terminals_buffer_radius = 100

    run(
        raw_gps_data_path,
        trip_terminals_data_path,
        terminals_buffer_radius,
    )
```

### 2. Pipeline to extract trips and stops details

```python
from gps2gtfs.pipeline.trip_stop import run


if __name__ == "__main__":
    raw_gps_data_path = "path/to/raw_gps_data/csv"
    trip_terminals_data_path = "path/to/trip_terminals_data/csv"
    stops_data_path = "path/to/stops_data/csv"
    terminals_buffer_radius = 100
    stops_buffer_radius = 50
    stops_extended_buffer_radius = 100

    run(
        raw_gps_data_path,
        trip_terminals_data_path,
        stops_data_path,
        terminals_buffer_radius,
        stops_buffer_radius,
        stops_extended_buffer_radius,
    )
```

<!-- ## More references

Please cite our work when you use;

S. Ratneswaran and U. Thayasivam, "Extracting potential Travel time information from raw GPS data and Evaluating the Performance of Public transit - a case study in Kandy, Sri Lanka," 2023 3rd International Conference on Intelligent Communication and Computational Techniques (ICCT), Jaipur, India, 2023, pp. 1-7, doi: https://doi.org/10.1109/ICCT56969.2023.10075789

## Note:

The raw GPS data set and processed GPS data sets are available upon request (contact: shiveswarran.22@cse.mrt.ac.lk)

--- -->

## License

MIT License

## Code of Conduct

Please read our [code of conduct document here](https://github.com/aaivu/aaivu-introduction/blob/master/docs/code_of_conduct.md).

[project]: https://img.shields.io/badge/-Project-blue
[research]: https://img.shields.io/badge/-Research-yellowgreen
