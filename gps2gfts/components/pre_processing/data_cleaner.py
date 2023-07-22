import pandas as pd


def raw_data_cleaning(raw_data):
    """
      Removal of records with error records.
      Remove data with zero values for longitude and latitude columns.
      Sort data by device id, date & time

      Args:
          raw_data (pd.DataFrame): Crude raw GPS data filtered out from the server for the required time window.

      Returns:
          gps_data (pd.DataFrame): A cleaned dataframe object of GPS data.
      """
    gps_data = raw_data[(raw_data['latitude'] != 0) & (raw_data['longitude'] != 0)].copy()
    gps_data['devicetime'] = pd.to_datetime(gps_data['devicetime'])
    gps_data['date'] = gps_data['devicetime'].dt.date
    gps_data['time'] = gps_data['devicetime'].dt.time
    gps_data.sort_values(by=['deviceid', 'date', 'time'], inplace=True)
    return gps_data
