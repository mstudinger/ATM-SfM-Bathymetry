# -*- coding: utf-8 -*-
"""
Created on Sat May 18, 2024

@author: Michael Studinger NASA, Goddard Space Flight Center 
         with code sections from C. Wayne Wright (https://github.com/lidar532) 

To import user-defined modules that are not located in the same folder as the main script use:
   
    import sys         
    # append the directory where this module is located to the sys.path list
    sys.path.append(r"<FULL_PATH_TO_FOLDER with asp_airborne_utilities.py>")       

usage in code:
    import atm_utilities
    df, header_data, lever_arm_sensor = atm_utilities.aux_reader(f_name_aux) # for function call
or
    from asp_airborne_utilities import df_temporal_search, aux_reader  # list required functions separated by commas
    result_df_temporal_search = df_temporal_search(aux_df,t_s,t_e,*args)  # for function call

"""

#%% helper function definition
# =============================================================================
# load ATM AUX file with all columns and extract header parameters into a class
# =============================================================================

def aux_reader(f_name_aux):
    """
    Summary: Read ATM AUX file and return header parameters as class and data as Pandas DataFrame.
             The auxiliary navigation files are included in NASA's Airborne Topographic Mapper (ATM) 
             CAMBOTv2 L0 data distribution and are freely available from the 
             National Snow and Ice Data Center (data set ID: IOCAM0):
             https://nsidc.org/data/iocam0/versions/1
             DOI: https://doi.org/10.5067/IOJH8A5F48J5
             
    Usage  : df, header_data, lever_arm_sensor = aux_reader(f_name_aux)

    INPUT:
    f_name_aux : string
        file name with location of ATM AUX file to be read 

    OUTPUT:
    df: DataFrame
        DataFrame with data from ATM AUX file
    header_data: class
        header parameters extracted from ATM AUX file
    lever_arm_sensor: array
        lever arm from GPS antenna phase center to the camera focal plane.
        for definition of lever arm see header of ATM AUX file.
    """

    # load the required modules
    
    import os
    import re
    import numpy as np
    import pandas as pd
        
    # parse header of ATM aux file and extract all information from header
    # this section of the code was written by C. Wayne Wright (https://github.com/lidar532)
    
    def parse_cambot_header(
        file_name:str,    # CAMBOTv2 file to read and extract header info from.
        max_chars=2000,   # Maximum number of characters to read in.
        debug:bool=False  # True to get debuggin printout, False for no debug printout
        ) -> object:      # A class containing the extracted data if it was found.
      """
      Parse a CAMBOT header and extract the fwd, right, down, pitch, roll, heading, Time_Offset, and Range_Bias values.
      and return a class with those values.
      asof: 2024-0214.
      """
    
      # regex expressions built with: https://regex101.com/
      rx_offset       = r"\[x-forward, y-starboard, z-down\]: (?P<fwd>-*\d+\.\d*), (?P<right>-*\d+\.\d+), *(?P<down>-*\d*\.\d*)"
      rx_attitude     = r"\[pitch, roll, heading\]: (?P<pitch>-*\d+\.\d*), *(?P<roll>-*\d*\.\d*), *(?P<heading>-*\d\.\d*)"
      rx_time_offset  = r"Time offset .*: *(?P<Time_Offset>-*\d\.\d*)"
      rx_range_bias   = r"Range bias.*: *(?P<Range_Bias>-*\d*\.*\d)"
      rx_file_name    = r"Input ancillary file: *(?P<aux_file_name>.*),"
      rx_header_row   = r"# *(ImageFilename)"
      row_number      = 0
    
      cb_fd = open(f_name_aux, 'r')
      cb_header = cb_fd.readlines(max_chars)
      if debug:
        for line in cb_header:
          print(f"line={line}", end="")
      cb_fd.close()
    
      # define a class to return the data we are able to extract
      class CB_HEADER():
        def __init__(self):
          self.header_row     = None
          self.fwd            = None
          self.right          = None
          self.down           = None
          self.pitch          = None
          self.roll           = None
          self.heading        = None
          self.Time_Offset    = None
          self.Range_Bias     = None
          self.header_row     = None
          self.data_start_row = None
          self.headers        = None
    
      # instantiate the return variable "rv" as a CB_HEADER class
      rv = CB_HEADER()
    
      # walk over the lines of the header
      for line in cb_header:
        if debug:
          print(f'{row_number:3d}: {line}', end='')
        x = re.search(rx_offset, line, flags=0)
        if x:
          rv.fwd   = float(x.group('fwd'))
          rv.right = float(x.group('right'))
          rv.down  = float(x.group('down') )
          if debug:
            print(f'        {rv.fwd = } {rv.right = } {rv.down = }')
    
        x = re.search(rx_attitude, line, flags=0)
        if x:
          rv.pitch   = float(x.group('pitch'))
          rv.roll    = float(x.group('roll'))
          rv.heading = float(x.group('heading'))
          if debug:
            print(f'      {rv.pitch = } {rv.roll = } {rv.heading = }')
    
        x = re.search(rx_time_offset, line, flags=0)
        if x:
          rv.Time_Offset = float(x.group('Time_Offset'))
          if debug:
            print(f'{rv.Time_Offset = }')
    
        x = re.search(rx_range_bias, line, flags=0)
        if x:
          rv.Range_Bias = float(x.group('Range_Bias'))
          if debug:
            print(f' {rv.Range_Bias = }')
    
        x = re.search(rx_file_name, line, flags=0)
        if x:
          rv.aux_file_name = x.group('aux_file_name')
          if debug:
            print(f' {rv.aux_file_name = }')
    
        x = re.search(rx_header_row, line, flags=0)
        if x:
          rv.row_number = row_number
          rv.header_row = line
          if debug:
            print(f' {row_number = }')
        row_number += 1
    
      if rv.header_row:
        rv.data_start_row = rv.row_number + 1
        rv.header_row = rv.header_row.strip()
        rv.headers = rv.header_row.replace("(", "_").replace(")", "").replace(" ", "").replace("#","").replace(">","").split(",")
      return rv
    
    # read header from ATM aux file and extract parameters
    header_data = parse_cambot_header(f_name_aux, debug=False )
          
    # extract lever arm parameters from class if they exist
    
    if (hasattr(header_data, 'fwd') &  hasattr(header_data, 'right') &  hasattr(header_data, 'down')):
        lever_arm_sensor = np.array([header_data.fwd, header_data.right, header_data.down])
    else:
        os.sys.exit("Unable to extract lever arm parameters from ATM aux file. Check input data.")
        
    # read data from ATM aux file
    df = pd.read_csv(f_name_aux, skiprows=header_data.data_start_row, names=header_data.headers)
 
    # some AUX files contain lon and lat at the beginning of the file that are zero. To remove them use:
    df = df.drop(df[np.abs(df.iloc[:, 3]) <= 0.5].index) # tested with WFF and other flights
    
    # NOTE: the column names for non-NSIDC data can be different from the NSIDC files
    # make consistent column labels to eliminate inconsisteny in the different input formats
    df.rename(columns={header_data.headers[0]: 'ID'}, inplace=True)
    df.rename(columns={header_data.headers[1]: 'Timestamp_UTC'}, inplace=True)
    df.rename(columns={header_data.headers[2]: 'PosixTime_UTC'}, inplace=True)
    df.rename(columns={header_data.headers[3]: 'gps_lat_deg'}, inplace=True)
    df.rename(columns={header_data.headers[4]: 'gps_lon_deg'}, inplace=True)
    df.rename(columns={header_data.headers[5]: 'gps_ele_m'}, inplace=True)
    df.rename(columns={header_data.headers[6]: 'gps_agl_m'}, inplace=True)
    df.rename(columns={header_data.headers[7]: 'roll_deg'}, inplace=True)
    df.rename(columns={header_data.headers[8]: 'pitch_deg'}, inplace=True)
    df.rename(columns={header_data.headers[9]: 'yaw_deg'}, inplace=True)
    
    #  return AUX data as Pandas DataFrame 
    return df, header_data, lever_arm_sensor

#%% helper function definition
# =============================================================================
# convert single UTC date string in ISO 8601 standard format to epoch seconds
# =============================================================================

def iso2epoch(date_str):
    """
    converts single UTC date string in ISO 8601 standard format (2019-05-12T16:10:40.5) 
    to epoch seconds a.k.a. POSIX time, defined as number of non-leap seconds 
    which have passed since 00:00:00 UTC on Thursday, January 1, 1970
    see: https://en.wikipedia.org/wiki/Unix_time
    
    Note: conversion must use an "aware" datetime object with the time zone defined (tzinfo=timezone.utc)
          using "naive" datetime objects without timezone information results in 
          conversion errors depending on the local time zone of the computer
    """
    
    from datetime import datetime
    from datetime import timezone
    
    if isinstance(date_str, str):    
        str_to_convert_dt = datetime.strptime(date_str.strip(),"%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)
        epoch_sec = str_to_convert_dt.timestamp() # convert to epoch seconds
    else:    
        print("Error: input argument must be a string in ISO 8601 standard format (2019-05-12T16:10:40.5)")
    
    return epoch_sec

#%% helper function definition
# =============================================================================
# locate UTC image timetags that match temporal search criteria
# =============================================================================

def df_temporal_search(aux_df,t_s,t_e,*args):
    """
    Summary     : locate UTC image timetags in POSIX timetag array that match temporal search criteria
    Usage       : result_df_temporal_search = df_temporal_search(aux_df,t_s,t_e,*args)
    Dependencies: iso2epoch from this module
    
    INPUT:
    aux_df : DataFrame created from ATM AUX file with function aux_reader()
        input must be a Pandas DataFrame with specific column names/order created by aux_reader()
    t_s : str
        UTC date string in ISO 8601 standard format (2019-05-12T16:10:40.5)
    t_e : str
        UTC date string in ISO 8601 standard format (2019-05-12T16:10:40.5)
    *args: bool
        optional input argument to display results from temporal search

    OUTPUT:
    result_df_temporal_search: class Result_DF_Temporal_Search()
        class with results of temporal search as attributes (defined below)
    """
    import sys
    import numpy as np
    
    # check for optional input arguments to display corresponding time window
    VERBOSE = False
    if len(sys.argv) >= 1:
        if isinstance(args[0], bool):
            VERBOSE = args[0]
                          
    # check if input aux_df is a Pandas DataFrame with expected column labels
    if hasattr(aux_df, 'gps_lon_deg') & hasattr(aux_df, 'gps_lat_deg') & hasattr(aux_df, 'PosixTime_UTC'):
        posix_utc = np.asarray(aux_df['PosixTime_UTC'])
    else:
        raise ValueError("\n\tERROR: input variable aux_df must be a DataFrame created with function aux_reader(). Abort.")

    t_s_posix = iso2epoch(t_s.strip()) # remove any white spaces at beginning or end
    t_e_posix = iso2epoch(t_e.strip())

    indx_inside_window = (posix_utc >= t_s_posix) & (posix_utc <= t_e_posix)

    # find indices where indx_time is True
    indx_list_temporal = [i for i, x in enumerate(indx_inside_window) if x]
    
    # verify that posix_utc time tags are increasing (is much faster than using diff apparently)
    if (np.all(posix_utc[1:] >= posix_utc[:-1])) == True:
        indx_s = indx_list_temporal[0]
        indx_e = indx_list_temporal[-1]
    else:
        raise ValueError("\n\tERROR: time tags are more monotonically increasing. Abort.")
    
    # define a class Result_DF_Temporal_Search for organizing the search results for return/output
    class Result_DF_Temporal_Search():
        def __init__(self):
            self.indx_inside_window  = None # boolean array with False outside the time window and True inside. same length as DataFrame
            self.indx_list_temporal  = None # list with indices of data points inside the time window
            self.indx_s              = None # first index of indx_list_spatial: indx_s = indx_list_temporal[0]
            self.indx_e              = None # last index of indx_list_spatial : indx_e = indx_list_temporal[-1]
            self.t_s_str             = None # time tag as type str of start of search window
            self.t_e_str             = None # time tag as type str of edn of search window
    
    # create return variable "result_df_temporal_search" as a Result_DF_Temporal_Search class
    result_df_temporal_search = Result_DF_Temporal_Search()
    
    # populate attributes in class
    result_df_temporal_search.indx_inside_window = indx_inside_window
    result_df_temporal_search.indx_list_temporal = indx_list_temporal
    result_df_temporal_search.indx_s             = indx_s
    result_df_temporal_search.indx_e             = indx_e
    result_df_temporal_search.t_s_str            = t_s
    result_df_temporal_search.t_e_str            = t_e
    
    return result_df_temporal_search
    
#%% helper function definition
# =============================================================================
# spatial search inside a polygon (provided as shapely object or DataFrame)
# =============================================================================

def df_spatial_search(aux_df,search_poly,*args):
    """
    Summary: locate UTC image timetags in navigation data that match spatial search criteria
    Usage  : result_df_spatial_search = df_spatial_search(aux_df,search_poly,*args)
    
    INPUT:
    aux_df : DataFrame created from ATM AUX file with function aux_reader()
        input must be a Pandas DataFrame with specific column names/order created by aux_reader()
    search_poly: TYPE
        closed search polygon for spatial search in geographic coordinates
        can be a) DataFrame or b) shapely Polygon object or c) n x 2 array (not yet implemented)
    *args: bool
        optional input argument to display corresponding time window for spatial search results

    OUTPUT:
    result_df_spatial_search: class Result_DF_Spatial_Search()
        class with results of spatial search as attributes (defined below)
    """
    
    import sys
    import numpy as np
    from shapely import geometry
    
    # check for optional input arguments to display corresponding time window
    VERBOSE = False
    if len(sys.argv) >= 1:
        if isinstance(args[0], bool):
            VERBOSE = args[0]
                          
    # check if input aux_df is a Pandas DataFrame with expected column labels
    if hasattr(aux_df, 'gps_lon_deg') & hasattr(aux_df, 'gps_lat_deg') & hasattr(aux_df, 'PosixTime_UTC'):
        gps_lat = np.asarray(aux_df['gps_lat_deg']) # latitude  in degrees of GPS antenna phase center (float64)
        gps_lon = np.asarray(aux_df['gps_lon_deg']) # longitude in degrees of GPS antenna phase center (float64)
        # make sure search polygon and aircraft GPS nav data are both wrapped to ±180°
        gps_lon = np.mod(gps_lon - 180.0, 360.0) - 180.0 
    else:
        raise ValueError("\n\tERROR: input variable aux_df must be a DataFrame created with function aux_reader(). Abort.")

    # check if input search_polygon is shapely polygon object
    # use pprint.pprint(search_polygon) to display type
    try:
        # access vertices of the polygon if needed
        x,y = search_poly.exterior.coords.xy 
    except:
        raise TypeError("\nERROR: input variable search_polygon must be a polygon object of\n       shapely.geometry.polygon module. Abort.")
       
    # allocate empty boolean array for faster loop
    indx_inside_poly = np.empty(len(gps_lon),dtype=bool)

    for i in range(len(gps_lon)):
        tmp_point = geometry.Point(gps_lon[i], gps_lat[i]) 
        indx_inside_poly[i] = search_poly.contains(tmp_point) or search_poly.touches(tmp_point)
        if VERBOSE:
            if indx_inside_poly[i] == True:
                print(f"found data inside search area with index: {i:d}")

    # find indices where indx_time is True
    indx_list_spatial = [i for i, x in enumerate(indx_inside_poly) if x]
    
    if VERBOSE:
        posix_utc = np.asarray(aux_df['PosixTime_UTC'])        
        # verify that posix_utc time tags are increasing (is much faster than using diff apparently)
        if (np.all(posix_utc[1:] >= posix_utc[:-1])) == True:
            indx_s = indx_list_spatial[0]
            indx_e = indx_list_spatial[-1]
        else:
            raise ValueError("\n\tERROR: time tags are more monotonically increasing. Abort.")
        
        t_s_str = aux_df['Timestamp_UTC'][indx_s]  
        t_e_str = aux_df['Timestamp_UTC'][indx_e]
        
        t_s_str = t_s_str.replace("T"," ")
        t_e_str = t_e_str.replace("T"," ")
        
        t_s_str = t_s_str.replace("-","/")
        t_e_str = t_e_str.replace("-","/")
        
        print(f"Start: {t_s_str[:-4]:s}")
        print(f"End  : {t_e_str[:-4]:s}")
    
    # define a class Result_DF_Spatial_Search for organizing the search results for return/output
    class Result_DF_Spatial_Search():
        def __init__(self):
            self.indx_inside_poly  = None # boolean array with False outside the area and True inside. same length as DataFrame
            self.indx_list_spatial = None # list with indices of data points inside the search area
            self.indx_s            = None # first index of indx_list_spatial: indx_s = indx_list_spatial[0]
            self.indx_e            = None # last index of indx_list_spatial: indx_e = indx_list_spatial[-1]
            self.t_s_str           = None # time tag as type str of first data point inside search area
            self.t_e_str           = None # time tag as type str of last  data point inside search area
    
    # create return variable "result_df_spatial_search" as a Result_DF_Spatial_Search class
    result_df_spatial_search = Result_DF_Spatial_Search()
    
    # populate attributes in class
    result_df_spatial_search.indx_inside_poly   = indx_inside_poly
    result_df_spatial_search.indx_list_spatial  = indx_list_spatial
    result_df_spatial_search.indx_s             = indx_s
    result_df_spatial_search.indx_e             = indx_e
    result_df_spatial_search.t_s_str            = t_s_str
    result_df_spatial_search.t_e_str            = t_e_str
    
    return result_df_spatial_search

# =============================================================================
# convert YR, DOY, SOD -> datetime object
# =============================================================================

from datetime import datetime
from datetime import timedelta

def kt19_to_datetime(yr, doy, sod, utc_offset):
    """
    input : YYYY, DOY, SOC_GPS, UTC_TO_GPS_OFFSET
    output: datetime object referenced to UTC
    NOTE  : assumes 10 Hz is the highest rate used in gitar derived trajectories
            this function is based on code from Matt Linkswiler with some improvements
    """
    yr   = int(yr)         # YYYY
    doy  = int(doy)        # DOY
    utc  = int(utc_offset) # UTC_TO_GPS_OFFSET

    # extract seconds and fraction of seconds and convert them to microseconds for datetime
    sod_gps, fff = divmod(sod, 1.0)   # note: sod >= 86400 is properly mapped into next day 
    # now convert fraction of seconds to microseconds (should be an integer for 10 Hz data)
    us = int(1000000 * round(fff, 1)) # rounding to 0.1 avoids numerical noise in divmod, but assumes max 10 Hz for gitar data 
     
    sod_utc = sod_gps - utc    # subtract UTC_TO_GPS_OFFSET from GPS to get UTC time base (only needed when processing GITAR data)

    dt = datetime(yr, 1, 1) + timedelta(doy - 1) + timedelta(seconds=sod_utc) + timedelta(microseconds=us)

    # change "naive" object to timezone-aware object by adding UTC time zone
    # note: DeprecationWarning: parsing timezone aware datetimes is deprecated; this will raise an error in the future
    # dt = dt.replace(tzinfo=timezone.utc)

    return dt