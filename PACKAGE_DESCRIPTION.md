# gps2gtfs: A Python package to process raw GPS data of public transit and transform to GTFS format

![project] ![research]

- <b>Project Lead(s) / Mentor(s)</b>

  1. Dr. T. Uthayasanker

- <b>Contributor(s)</b>
  1. R. Shiveswarran
  2. S. Gopinath
  3. S. Kajanan
  4. A. Kesavi

## Description

<div style="text-align: justify;">
The "gps2gtfs" Python package provides a streamlined solution for preprocessing GPS (Global Positioning System) raw data and converting it into GTFS (General Transit Feed Specification) data format. Leveraging the power of DataFrame and GeoDataFrame with parallelization, this package offers efficient methods to extract essential trip details from raw GPS data. These details encompass trip sequences, stop information, arrival time to stops, departure time from stops, dwell time at stops, travel durations, running times between stops, and the seamless transformation into GTFS data structure. Currently, "gps2gtfs" handles static (schedule) trip data at heterogeneous traffic condition, with the potential for future expansion to accommodate dynamic real-time trip data. Furthermore, in the future, a visualization package can be seamlessly integrated with existing packages.
</div>

<br>

<b>Keywords:</b> GTFS, GPS, Travel Time, Public Transit, Heterogeneous Traffic Condition, ITS (Intelligent Transportation System)

## Architecture

<div style="text-align: justify;">
The "gps2gtfs" framework is developed using Python 3, with a thoughtfully designed package structure that ensures minimal interdependence among the main packages. The core components encompass distinct packages, each serving a specific purpose: data_field, load_data, preprocessing, trip, stop, reporting, pipeline, and utility. Users are expected to provide input for a single route, and the system facilitates the inclusion of multiple routes into the pipeline through user-driven iteration.
</div>

<br>

The package is structured into eight(8) primary packages:

1. <b>data_field:</b> This package is responsible for managing column names for user input and a predefined set of output columns. The fields provided by the user should be a superset of the defined fields within this package.
2. <b>load_data:</b> This package handles the loading of necessary data into the pipeline.
3. <b>preprocessing:</b> The preprocessing package is designed to clean the data loaded from the previous step.
4. <b>trip:</b> The trip package focuses on extracting trips and generating associated features.
5. <b>stop:</b> Within the stop package, the identification of stops and the creation of related features take place.
6. <b>reporting:</b> This package is responsible for generating outputs containing the extracted information.
7. <b>pipeline:</b> This package contains functionality to execute the trip extraction pipeline and the trip & stop extraction pipeline.
8. <b>utility:</b> The utility module provides support for various utility functions, including input/output operations, data conversions, and logging.


### Architecture digram of gps2gfts

<img width="1000" alt="img1" src="https://github.com/aaivu/gps2gtfs/assets/74850246/678af0a8-64e3-49b5-8fb6-66b331ea7cae" >

<hr>

### How the gps2gfts works

<img width="1000" alt="img2" src="https://github.com/aaivu/gps2gtfs/assets/74850246/92cf2e62-2be4-49e1-b401-78ebbe20d194">

<br>

## Quick Example

It is essential to provide input files in CSV format for proper functionality. Additionally, the utilization of this package requires the presence of a main thread.

### 1. Pipeline to extract trips details

```py
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

<hr>

### 2. Pipeline to extract trips and stops details

```py
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

MIT License. You can see [here](https://github.com/aaivu/gps2gtfs/blob/master/LICENSE).

## Code of Conduct

Please read our [code of conduct document here](https://github.com/aaivu/aaivu-introduction/blob/master/docs/code_of_conduct.md).

[project]: https://img.shields.io/badge/-Project-blue
[research]: https://img.shields.io/badge/-Research-yellowgreen
