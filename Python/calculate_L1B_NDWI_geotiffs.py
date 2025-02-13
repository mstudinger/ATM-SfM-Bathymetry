# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11, 2025

@author: Michael Studinger, NASA - Goddard Space Flight Center

This Python™ code is designed to work with the ATM L1B data product available at:
    
    https://nsidc.org/data/iocam1b/versions/2
    IceBridge CAMBOT L1B Geolocated Images, Version 2
    Data set id: IOCAM1B
    DOI: 10.5067/B0HL940D452L

Purpose: create georeferenced NDWI_ice GeoTiff images from the above data product
    For information about the Normalized Difference Water Index modified for ice (NDWIice) see:
    https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_lake_detection_using_NDWI_and_Otsu_thresholding.ipynb
    
"""

#%% load required modules

import rioxarray# as rio
import numpy as np
import os

VERBOSE = False

#%% set input and output files names

f_dir_L1b   = r"CAMBOT_L1"
f_name_list = f_dir_L1b + os.sep + "f_name_list_to_mosaic.txt" 


#%% set file name prefix depening on files 

#FILE_TYPE = "RAMP" # "NSIDC" or "RAMP"
FILE_TYPE = "NSIDC" # or "RAMP"

if FILE_TYPE == "NSIDC":
    f_name_start = "IOCAM1B"
elif FILE_TYPE == "RAMP":
    f_name_start = "2019"
    
#%% extract R, G, and B bands for calculating NDWI output data set

def extract_band_from_GeoTiff(rgb_array, band1, band2):
    
    """
    extract a single band from an RGB geotiff DataArray that has been imported with rioxarray
    and return a single channel DataArray as dtype float32 for NDWI calculation
    """
    
    # set bands to delete (e.g., bands 1, 2, and 3, are RGB
    bands_to_delete = [band1, band2] # band numbers start at 1 - check size of masked DataArray
    # create a mask to keep desired band(s)
    mask = np.ones(rgb_array.shape[0], dtype = bool)
    mask[np.array(bands_to_delete) - 1] = False
    # apply the mask to remove bands
    d_array_out = rgb_array[mask, :, :]
    # update the 'band' coordinate to reflect the remaining bands
    d_array_out['band'] = np.arange(1, d_array_out.shape[0] + 1)
    # set the nodata value 
    d_array_out.rio.write_nodata(0, inplace = True)  # works for display in QGIS
    
    d_array_out.values[:,:].astype("float32")        # both lines of code seem to be needed
    d_array_out.astype("float32")                    # to work properly

    return d_array_out

#%% make list with file names to convert

# r = root, d = directories, f = files

# start with empty list of file names
list_of_files = []

for r, d, f in os.walk(f_dir_L1b): 
        for file in sorted(f):
            if (file.startswith(f_name_start) & file.endswith(".tif") & (file.count("ndwi") == 0)):
                f_name_inp = f_dir_L1b + os.sep + file
                f_name_out = f_dir_L1b + os.sep + file.replace(".tif","_ndwi.tif")
                print(file)
                list_of_files.append(file)

                # load data into a DataArray
                rgb = rioxarray.open_rasterio(f_name_inp, chunks=True, lock=False)

                # call function and extract bands          
                ndwi = extract_band_from_GeoTiff(rgb, 1, 3) # keeps green channel for NDWI
                red  = extract_band_from_GeoTiff(rgb, 2, 3) # red channel
                blue = extract_band_from_GeoTiff(rgb, 1, 2) # blue channel

                # calculate NDWI - convert DataArray type into numpy array            
                RED  = np.asarray(red.values,dtype=float)  
                BLUE = np.asarray(blue.values,dtype=float)
                
                # replace 0 values (nodata) with NaNs to avoid warning message dividing by 0
                RED  = np.where(RED  == 0, np.nan, RED)
                BLUE = np.where(BLUE == 0, np.nan, BLUE)
                
                NDWI = (BLUE - RED)/(BLUE + RED)
                ndwi.values = NDWI
                
                # fix NaN value in NDWI
                ndwi.rio.write_nodata(np.nan, inplace = True) # works for display in QGIS

                # fix CRS with proper EPSG code                
                # not needed here. simplistic but works
                # if (rgb.spatial_ref.standard_parallel == 70.0 and rgb.spatial_ref.straight_vertical_longitude_from_pole == -45.0):
                #    print('CRS parameters verified')
                
                if (rgb.spatial_ref.crs_wkt == 'PROJCS["unnamed",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",70],PARAMETER["central_meridian",-45],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1],AXIS["Easting",SOUTH],AXIS["Northing",SOUTH]]'):
                    ndwi.rio.write_crs("epsg:3413", inplace=True)
                    if VERBOSE:
                        print("\n\tUpdated CRS EPSG code in exported file based on NSIDC WKT verification.")
                    
                # save GeoTiff files as float32 with LZW compression and updated statistics
                # also seems to properly recognize NaN as the nodata value
                # and seems to set dtype right, which results in larger file size even with LZW compression
                
                ndwi.rio.to_raster(f_name_out, dtype="float32", driver="GTiff", compress="LZW") 

#%% save list with file names to use with ASP dem_mosaic

f_obj = open(f_name_list, 'w',newline='\n') # use Unix-style LF end-of-line terminators from Windows

for i in range(len(list_of_files)):
    f_obj.write(f'{list_of_files[i]:s}\n')
f_obj.close()

#%% now run ASP dem_mosaic
# https://stereopipeline.readthedocs.io/en/latest/tools/dem_mosaic.html

