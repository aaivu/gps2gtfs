import geopandas as gpd


def convert_to_geo_data_frame(data_frame):
    # converting to GeoDataframe with Coordinate Reference system 4326
    data_frame = gpd.GeoDataFrame(data_frame, geometry=gpd.points_from_xy(data_frame.longitude, data_frame.latitude),
                                  crs='EPSG:4326')
    # project them in local coordinate system
    return data_frame.to_crs('EPSG:5234')


def geo_buffer_extend(data_frame, buffer_size):
    return gpd.GeoDataFrame(data_frame, geometry=data_frame.geometry.buffer(buffer_size))
