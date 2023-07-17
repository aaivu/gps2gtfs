"""GPS datapreprocessing & Trip extraction

Bus trip extraction from GPS data

Importing python libraries
"""
! pip install geopandas

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime,date
import geopandas as gpd
from geopandas import GeoDataFrame as gdf
from google.colab import files
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster

import glob
import os



def get_data(path: str)  ->  pd.DataFrame:

  """
    Get csv file from given file path.
    
    Args:
        path (str): Location for the file.
    
    Returns:
        data (pd.DataFrame): A DataFrame Object of given file path.
    """

  data = pd.read_csv(path)
  return data


def raw_data_cleaning(raw_data: pd.DataFrame) -> pd.DataFrame:

  """
    Removal of records with error records. 
    Remove data with zero values for longitude and latitude columns.
    Sort data by time and device.
    
    Args:
        raw_data (pd.DataFrame): Crude raw GPS data filtered out from the server for the required time window.
    
    Returns:
        gps_data (pd.DataFrame): A cleaned dataframe object of GPS data.
    """
  
  #raw_data = raw_data.drop(drop_columns, axis = 1)

  gps_data = raw_data[raw_data.latitude != 0]
  gps_data = gps_data[gps_data.longitude != 0] #cleaning zero values for latitude & longitude

  gps_data['date'] = pd.to_datetime(gps_data['devicetime']).dt.date #split date and time separately into datetime variables
  gps_data['time'] = pd.to_datetime(gps_data['devicetime']).dt.time

  gps_data = gps_data.sort_values(['deviceid', 'date', 'time']) #sorting dataset by time and device

  return gps_data



def trip_ends(gps_data: pd.DataFrame, bus_terminals: pd.DataFrame, end_buffer: int) -> pd.DataFrame:

  """
    To extract trip ends dataframe with given buffer range.
    Filter the records within terminals selected buffer range. 
    Within the filtered records get entry & exit to terminals.


    Args:
        gps_data (pd.DataFrame): Cleaned gps data filtered out from the server for the required time window.
        bus_terminals (pd.DataFrame): End and start terminals for the trip.
        end_buffer (int):  Radius of the buffer area to represent terminals.
    
    Returns:
        trip_ends (pd.DataFrame): Trip data with extracted terminals.
  """

  #converting to GeoDataframe with Coordinate Reference system 4326 
  gps_data = gpd.GeoDataFrame(gps_data, geometry=gpd.points_from_xy(gps_data.longitude,gps_data.latitude),crs='EPSG:4326')
  bus_terminals = gpd.GeoDataFrame(bus_terminals, geometry=gpd.points_from_xy(bus_terminals.longitude,bus_terminals.latitude),crs='EPSG:4326') 
  
  #project them in local cordinate system
  gps_data = gps_data.to_crs('EPSG:5234')
  bus_terminals = bus_terminals.to_crs('EPSG:5234')

  #creating buffer area to extract records around bus terminals
  bus_terminals_buffer = gpd.GeoDataFrame(bus_terminals, geometry = bus_terminals.geometry.buffer(end_buffer))

  #filtering coordinates within bus terminals end buffer
  gps_data['bus_stop'] = pd.Series(dtype='object') #create a new column in gps data set
  gps_data.reset_index(drop = True, inplace = True) #reset indices to run a for loop

  for i in range(len(gps_data)):
    for stop in range(len(bus_terminals)):
      if bus_terminals_buffer.iloc[stop].geometry.contains(gps_data.iloc[i].geometry):
        gps_data.at[i,'bus_stop'] = bus_terminals.at[stop,'terminal_id']

  trip_ends = gps_data.dropna() #filter records within terminal buffer

  #EXTRACT TRIP ENDS

  #grouping the filtered records of one bus terminal and one date
  trip_ends['grouped_ends'] = ((trip_ends['bus_stop'].shift() != trip_ends['bus_stop']) | (trip_ends['date'].shift() != trip_ends['date'])).cumsum()

  #find the entry or exit record only of the terminals
  #Early records is the entry(1) to the terminal and last record as the exit(0) to the end terminal 
  trip_ends['entry/exit'] = pd.Series(dtype='object')
  trip_ends = trip_ends.reset_index(drop=True)

  for name, group in trip_ends.groupby('grouped_ends'):
    #if 0 in group['speed'].values:
    for index, row in group.iterrows():
      if row['devicetime'] == group['devicetime'].max():
        trip_ends.at[index,'entry/exit'] = '0'
      elif row['devicetime'] == group['devicetime'].min():
        trip_ends.at[index,'entry/exit'] = '1'
  
  trip_ends = trip_ends.dropna() #filter terminal entry/exit records only 
  
  trip_ends = trip_ends.reset_index(drop=True)

  #Providing unique trip id for trips which have entry / exit values within the 2 bus end terminals
  trip = 0
  for i in range(len(trip_ends)-1):
    if (trip_ends.at[i,'bus_stop'] != trip_ends.at[i+1,'bus_stop']) & (trip_ends.at[i,'date'] == trip_ends.at[i+1,'date']):
      trip= trip+1
      trip_ends.at[i,'trip_id'] = trip
      trip_ends.at[i+1,'trip_id'] = trip

  trip_ends = trip_ends.dropna()

  trip_ends = trip_ends.groupby('trip_id').filter(lambda x : len(x)>1)    #remove outliers where no defined 2 trip ends for a trip
  trip_ends = trip_ends.reset_index(drop=True)

  return trip_ends

def download_csv(data: pd.DataFrame, filename: str) -> None:

  """
    To download output as CSV files 

    Args:
        data (pd.DataFrame): DataFrame Object.
        filename (str): Name of the file has to be faved.
    
    Returns:
        None
  """
    
  filename= filename + '.csv'
  data.to_csv(filename, encoding = 'utf-8-sig',index= False)
  files.download(filename)



def trip_extraction(trip_ends: pd.DataFrame) -> pd.DataFrame:
  
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
  bus_trips[['end_time','end_terminal']] = bus_trips[['time','bus_stop']].shift(-1)
  bus_trips = bus_trips.iloc[::2]

  bus_trips = bus_trips.drop(['id','devicetime','latitude','longitude','speed','geometry','grouped_ends','entry/exit'],axis=1)
  bus_trips.insert(0,'trip_id',bus_trips.pop('trip_id'))
  bus_trips.rename(columns = {'time':'start_time','bus_stop': 'start_terminal'}, inplace =True)

  conditions = [(bus_trips['start_terminal'] == 'BT01'),
              (bus_trips['start_terminal'] == 'BT02')]
  values = [1,2]

  bus_trips['direction'] = np.select(conditions, values)

  bus_trips = bus_trips[['trip_id','deviceid','date','start_terminal','end_terminal','direction','start_time','end_time']]
  bus_trips=bus_trips.reset_index(drop = True)

  #Calculate trip duration
  bus_trips['duration'] = pd.Series(dtype='object')
  for i in range(len(bus_trips)):
    bus_trips.at[i,'duration'] = datetime.combine(date.min,bus_trips.at[i,'end_time']) - datetime.combine(date.min,bus_trips.at[i,'start_time'])
  
  bus_trips['duration_in_mins'] = bus_trips['duration']/np.timedelta64(1,'m')

  bus_trips['day_of_week'] = pd.to_datetime(bus_trips['date']).dt.weekday
  bus_trips['hour_of_day'] = list(map(lambda  x: x.hour, (bus_trips['start_time'])))
  
  return bus_trips





def map_visualization(gps_data, city_location, bus_terminals, bus_terminals_buffer):

  """
    Using a  GPS data visualization package of Folium, project the coordinates on 
    Open Street Map (OSM) to explore how the records are spread and to gain some insights and overview.

    Args:
        gps_data (pd.DataFrame): GPS data with selected device ID.
        city_location (list): Longtitude and lattitude of a city
        bus_terminals (GeoDataFrame) : Bus terminal data with geometry column
        bus_terminals_buffer (GeoDataFrame) :  Bus terminal data with geometry column buffer range      
    
    Returns:
        map (MapObject): A visualizable Map Object.
  """
    
  gps_data = gpd.GeoDataFrame(gps_data, geometry=gpd.points_from_xy(gps_data.longitude,gps_data.latitude),crs='EPSG:4326')  #converting to GeoDataframe with Coordinate Reference system 4326
  map =  folium.Map(location=city_location, tiles='openstreetmap', zoom_start=14)
  for idx, row in gps_data.iterrows():
    Marker([row['latitude'], row['longitude']]).add_to(map)
  
  bus_terminals = gpd.GeoDataFrame(bus_terminals, geometry=gpd.points_from_xy(bus_terminals.longitude,bus_terminals.latitude),crs='EPSG:4326')
  for idx, row in bus_terminals.iterrows():
    Marker([row['latitude'], row['longitude']]).add_to(map)

  folium.GeoJson(bus_terminals_buffer.to_crs(epsg=4326)).add_to(map)
  map
  return map




if __name__=="__main__":
  
  path_raw_data = '/content/drive/Shareddrives/MSc - Shiveswarran/Raw Data/kadugannawa_2022_10.csv'
  path_bus_terminals = '/content/drive/Shareddrives/MSc - Shiveswarran/Raw Data/bus_terminals_690.csv'

  raw_data = get_data(path_raw_data)
  bus_terminals = get_data(path_bus_terminals)

  gps_data= raw_data_cleaning(raw_data)

  end_buffer = 100
  trip_ends = trip_ends(gps_data,bus_terminals,end_buffer)
  download_csv(trip_ends,'trip_ends')

  bus_trips = trip_extraction(trip_ends)
  download_csv(bus_trips,'bus_trips')

  bus_terminals = gpd.GeoDataFrame(bus_terminals, geometry=gpd.points_from_xy(bus_terminals.longitude,bus_terminals.latitude),crs='EPSG:4326') 
  bus_terminals = bus_terminals.to_crs('EPSG:5234')
  bus_terminals_buffer = gpd.GeoDataFrame(bus_terminals, geometry = bus_terminals.geometry.buffer(end_buffer))

  gps_data['deviceid'].value_counts()

  data84 = gps_data[gps_data['deviceid']==84]

  city_location = [7.2906,80.6337]  #Kandy city location
  map = map_visualization(data84,city_location,bus_terminals,bus_terminals_buffer)

  map

