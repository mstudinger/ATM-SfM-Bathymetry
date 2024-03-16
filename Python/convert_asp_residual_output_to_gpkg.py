# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: Michael Studinger, NASA - Goddard Space Flight Center
"""
import numpy as np
import pandas as pd
import geopandas as gpd

#%% CSV format of ASP residual output files:

# # lon, lat, height_above_datum, mean_residual, num_observations
# # Geodetic Datum --> Name: WGS_1984  Spheroid: WGS 84  Semi-major axis: 6378137  Semi-minor axis: 6356752.3142451793  Meridian: Greenwich at 0  Proj4 Str: +proj=longlat +datum=WGS84 +no_defs
# -49.484664401690743, 69.03132509404557, 589.7272955584134, 0.050144369704773345, 2
# -49.484581031768634, 69.031355986109517, 589.19529987134808, 0.08165516527643793, 2


#%% import ASP residual data file in CSV format into data frame

def convert_asp_res_to_gpkg(
    f_name_res:str,   # ASP residual data file in CSV format
    ):      

    """
      read ASP residual output file in CSV format into data frame,
      and save as GeoPackage (GPKG) file for plotting with GIS software.
    """

    try:
      res_df = pd.read_csv(f_name_res, sep=',', header=0, skiprows=[1])
      # clean up column names
      res_df.columns = res_df.columns.str.replace('#', '')
      res_df.columns = res_df.columns.str.replace(' ', '')
    except:
      print(f'Unable to read {f_name_res}. Check path and input file name.')
        
    # wrap longitudes to ±180 degrees for GeoPackage (GPKG) export with geographic coordinates
    res_df['lon'] = np.mod(res_df['lon'] - 180.0, 360.0) - 180.0 
    
    # populate GeoDataFrame
    res_gdf = gpd.GeoDataFrame(res_df, geometry=gpd.points_from_xy(res_df['lon'], res_df['lat']))
    
    # remove latitude and longitude colums since they are stored in geometry -> smaller files = faster load in QGIS
    res_gdf = res_gdf.drop(columns=['lon'])
    res_gdf = res_gdf.drop(columns=['lat'])
    
    # set up the WGS-84 geographic coordinate system
    res_gdf = res_gdf.set_crs("EPSG:4326") # need to wrap longitudes to ±180 degrees for geopgraphic coordinates
    
    # save GeoPackage (GPKG) file
    res_gdf.to_file(f_name_out, driver="GPKG")


#%% run module/function as script 

if __name__ == '__main__':
    
    import os
    f_name_res = r".." + os.sep + "data" + os.sep + "example_files" + os.sep + "asp_ba_out-final_residuals_pointmap.csv"
    f_name_out = f_name_res.replace(".csv", ".gpkg")

    # execute function    
    convert_asp_res_to_gpkg(f_name_res)

