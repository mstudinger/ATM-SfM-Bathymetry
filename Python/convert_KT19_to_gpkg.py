# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13, 2024

@author: Michael Studinger, NASA - Goddard Space Flight Center

Purpose: Python™ function/script to convert surface temperature measurements from ATM's 
         Heitronics KT19.85 Series II Infrared Radiation Pyrometer 
         to GeoPackage (GPKG) format.

Data:    Data are freely available from the National Snow and Ice Data Center (NSIDC) 
         Data set ID: IAKST1B
         https://nsidc.org/data/IAKST1B
         DOI: https://doi.org/10.5067/UHE07J35I3NB
         Documentation: https://nsidc.org/sites/default/files/iakst1b-v002-userguide_0.pdf

Note:   An example data file is included in this repository in the folder 
        data/example_files and is used in this script for demonstration:
        IAKST1B_KT19_PROCESSED_20190506_102239.txt

"""

import time
import numpy as np
import pandas as pd
import geopandas as gpd
from   asp_airborne_utilities import kt19_to_datetime

#%% function to import KT19 ASCII file from NSIDC, convert to GeoDataFrame 
#   and export as GeoPackage (GPKG) file if desired

def kt19_to_gdf(
    f_name_kt19_inp:str,    # path to KT19 ASCII text file from NSIDC
    EXPORT_GIS:bool,        # GeoPackage (GPKG) file if True
    ):      

    """
      read KT19 ASCII data file, convert it to GeoDataFrame, and save data as 
      GeoPackage (GPKG) file if desired.
    """

    try:
        kt19_df = pd.read_csv(f_name_kt19_inp, skiprows = 10)
    except:
        print(f'Unable to read {f_name_kt19_inp}. Check path and input file name.')
          
    # clean up column names
    for i in range(len(kt19_df.columns)):
        kt19_df.rename(columns={kt19_df.columns[i]: kt19_df.columns[i].replace("(", "_").replace(")", "").replace("#","").replace(" ", "").lower()},inplace=True)
    
    # create empty datetime object for memory allocation for faster loop execution
    utc_time = np.empty(len(kt19_df), dtype='datetime64[ns]')
    
    for k in range(len(kt19_df)):
        utc_time[k] = kt19_to_datetime(kt19_df["year"][k], kt19_df["day_of_year"][k], kt19_df["seconds_of_day_utc"][k], 0)
    
    kt19_df["utc_time"] = utc_time
    
    # need to wrap longitudes to ±180° for exporting geographic coordinates 
    # 0° to 360° is not supported for GeoPackage (GPKG) format
    kt19_df["longitude_deg"] = np.mod(kt19_df["longitude_deg"] - 180.0, 360.0) - 180.0
    
    # populate lat lon geometry in GeoDataFrame
    kt19_gdf = gpd.GeoDataFrame(kt19_df, geometry=gpd.points_from_xy(kt19_df["longitude_deg"], kt19_df["latitude_deg"]))
    
    # remove redundant lon lat columns for smaller file size and faster loading in QGIS
    kt19_gdf.drop(columns=["longitude_deg","latitude_deg"],inplace=True)
    
    # set the coordinate system
    # EPSG:4326 WGS84 - World Geodetic System 1984, used in DGPS solutions for ATM geolocation
    kt19_gdf = kt19_gdf.set_crs("EPSG:4326")
    
    # if desired export file as GeoPackage - note: fractional seconds are not exported in utc_time field
    if EXPORT_GIS:
        f_name_kt19_out = f_name_kt19_inp.replace(".txt",".gpkg")
        tic = time.perf_counter()
        kt19_gdf.to_file(f_name_kt19_out, driver="GPKG")
        toc = time.perf_counter()
        print(f"Time to save GeoPackage GPKG file: {toc - tic:0.1f} seconds")       

    return kt19_gdf

#%% run module/function as script 

if __name__ == '__main__':
    
    f_name_kt19_inp = r"..\data\example_files\IAKST1B_KT19_PROCESSED_20190506_102239.txt"
    
    # set processing options
    EXPORT_GIS = True

    # execute function    
    kt19_gdf = kt19_to_gdf(f_name_kt19_inp,EXPORT_GIS)


