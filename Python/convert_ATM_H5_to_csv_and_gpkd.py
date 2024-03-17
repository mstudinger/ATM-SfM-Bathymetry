# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16, 2024

@author: Michael Studinger, NASA - Goddard Space Flight Center

This Python™ function/script is designed to work with these two NASA data products:
https://nsidc.org/data/ilatm1b/versions/2
https://nsidc.org/data/ilnsa1b/versions/2

The code reads the following four fields from the ATM ilatm1b and ilnsa1b HDF5 files:
    
/longitude: laser spot longitude in degrees east
/latitude:  laser spot latitude in degrees north
/elevation: elevation of the laser spot above ellipsoid in meters
/instrument_parameters/rcv_sigstr: Received Laser Signal Strength (relative). This is the sum taken over the received pulse of the waveform samples in units of digitizer counts.

"""

#%% import required modules

import h5py
import time
import numpy as np
import pandas as pd
import geopandas as gpd

#%% define function for reading and converting ATM NSIDC data products in HDF5 format
    
def convert_atm_H5_to_csv_and_gpkg(
    f_name_atm:str,   # path to ATM point cloud lidar file in HDF5 format
    EXPORT_CSV:bool,  # if True = CSV output
    EXPORT_GIS:bool,  # if True = GPKG output
    ANGLE_WRAP:float, # wrap longitudes to ±180° or 0°-360°. ANGLE_WRAP variable must either be 180 or 360
    ):      

    """
      read ATM HDF5 L1B data file, convert it to data frame, and save data as CSV and/or,
      GeoPackage (GPKG) file for plotting with GIS software.
    """

    try:
      data_hdf_atm = h5py.File(f_name_atm, 'r')
      # read necessary data fields
      lon = data_hdf_atm['/longitude'][:]
      lat = data_hdf_atm['/latitude'][:]
      ele = data_hdf_atm['/elevation'][:]
      sig = data_hdf_atm['/instrument_parameters/rcv_sigstr'][:]
      
      f_name_csv = f_name_atm.replace(".h5",".csv")
      f_name_gis = f_name_atm.replace(".h5",".gpkg")
    except:
      print(f'Unable to read {f_name_atm}. Check path and input file name.')
        
    # assemble numpy array    
    atm_data = np.block([lon[:,np.newaxis],lat[:,np.newaxis],ele[:,np.newaxis], sig[:,np.newaxis]])
    # convert numpy array to dataframe 
    atm_df = pd.DataFrame(data = atm_data, columns =["lon_deg", "lat_deg", "ele_m", "sigstr_cts"]) 
      
    # save CSV file if desired    
    if EXPORT_CSV:
        header_list = [atm_df.columns[0],atm_df.columns[1],atm_df.columns[2],atm_df.columns[3]]
        header_str = ','.join(header_list)
        
        if ANGLE_WRAP == 180:   # wrap longitudes to ±180°
            atm_data[:,0] = np.mod(atm_data[:,0] - 180.0, 360.0) - 180.0
        elif ANGLE_WRAP == 360: # wrap longitudes to 0°-360°
            atm_data[:,0] = atm_data[:,0] % 360
        else:
            import os
            os.sys.exit("Parameter ANGLE_WRAP must must either be 180 or 360. Abort.")
            
        tic = time.perf_counter()    
        np.savetxt(f_name_csv, X = atm_data, header = header_str, comments='', delimiter=",", fmt = ['%14.9f', '%14.9f' , '%10.4f', '%6.0f'])
        toc = time.perf_counter()
        print(f"\tTime to save ASCII (CSV) file: {toc - tic:0.1f} seconds")
        
    # save GeoPackage (GPKG) file with geographic coordinates if desired   
    if EXPORT_GIS:
        
        # wrap longitudes to ±180° for GeoPackage (GPKG) export with geographic coordinates. 0°-360° is not supported.
        atm_df['lon_deg'] = np.mod(atm_df['lon_deg'] - 180.0, 360.0) - 180.0 
        
        # populate GeoDataFrame
        atm_gdf = gpd.GeoDataFrame(atm_df, geometry=gpd.points_from_xy(atm_df['lon_deg'], atm_df['lat_deg']))
    
        # remove redundant latitude and longitude columns since coordinates are stored in geometry -> smaller files = faster load in QGIS
        atm_gdf = atm_gdf.drop(columns=['lon_deg'])
        atm_gdf = atm_gdf.drop(columns=['lat_deg'])
        
        # set up the WGS-84 geographic coordinate system
        atm_gdf = atm_gdf.set_crs("EPSG:4326") # need to wrap longitudes to ±180° for geopgraphic coordinates. 0°-360° is not supported.
        
        # save GeoPackage (GPKG) file    
        tic = time.perf_counter()
        atm_gdf.to_file(f_name_gis, driver="GPKG")
        toc = time.perf_counter()
        print(f"\tTime to save GeoPackage (GPKG) file: {toc - tic:0.1f} seconds")
    
#%% run module/function as script 

if __name__ == '__main__':
    
    import os
    f_name_atm = r".." + os.sep + "data" + os.sep + "example_files" + os.sep + "ILATM1B_20190506_131600.ATM6AT6.h5"
    
    # set processing options
    EXPORT_CSV = True
    EXPORT_GIS = True
    ANGLE_WRAP = 180.0 # wrap longitudes to ±180° or 0°-360°. ANGLE_WRAP variable must either be 180 or 360

    # execute function    
    convert_atm_H5_to_csv_and_gpkg(f_name_atm,EXPORT_CSV,EXPORT_GIS,ANGLE_WRAP)
