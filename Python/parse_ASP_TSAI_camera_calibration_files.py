# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20, 2024

@author: Michael Studinger, NASA Goddard Space Flight Center
"""

# import required modules
import re

def parse_asp_tsai_file(
    f_name:str,   # ASP camera calibration file using the Tsai camera calibration technique
    ) -> object:  # a class containing the extracted parameters that were found

    """
      Parse ASP camera calibration file using the Tsai camera calibration technique,
      extract parameters, and return a class with the extracted values that were found.
    """
    
    # read camera/lens calibration file for parsing
    lens_cal = open(f_name, 'r')
    tsai_info = lens_cal.readlines() # reads the entire file
    lens_cal.close()
    
    # define a class TsaiParams for organizing the extracted lens calibration parameters
    class TsaiParams():
        def __init__(self):
            self.fu    = None
            self.fv    = None
            self.cu    = None
            self.cv    = None
            self.k1    = None
            self.k2    = None
            self.p1    = None
            self.p2    = None
            self.pitch = None
    
    # create return variable "tsai_params" as a TsaiParams class
    tsai_params = TsaiParams()
    
    # the code for parsing the lens calibration files was inspired 
    # by C. Wayne Wright's (https://github.com/lidar532) function:
    # parse_cambot_header in the Jupyter notebook:
    # https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_convert_GPS_to_camera_pos.ipynb
    
    # define search patterns and group names
    # to develop/verify search patterns with https://regex101.com/ make sure to select
    # Python™ in the "FLAVOR" tab on the left and then use the string inside r"":
    rx_fu = r"fu = (?P<fu>.\d*\.*\d*)" 
    rx_fv = r"fv = (?P<fv>.\d*\.*\d*)"
    rx_cu = r"cu = (?P<cu>.\d*\.*\d*)"
    rx_cv = r"cv = (?P<cv>.\d*\.*\d*)"
    rx_k1 = r"k1 = (?P<k1>.\d*\.*\d*)" # includes positive and negative values
    rx_k2 = r"k2 = (?P<k2>.\d*\.*\d*)"
    rx_p1 = r"p1 = (?P<p1>.\d*\.*\d*)"
    rx_p2 = r"p2 = (?P<p2>.\d*\.*\d*)"
    
    # read pitch value. if pitch = 1.0 units for focal length etc. are in pixels
    rx_pitch = r"pitch = (?P<pitch>.\d*\.*\d*)"  
    
    for line in tsai_info:
        
        re_srch = re.search(rx_fu, line, flags=0)
        if re_srch:
            tsai_params.fu = float(re_srch.group('fu'))
        
        re_srch = re.search(rx_fv, line, flags=0)
        if re_srch:
            tsai_params.fv = float(re_srch.group('fv'))
            
        re_srch = re.search(rx_cu, line, flags=0)
        if re_srch:
            tsai_params.cu = float(re_srch.group('cu'))        
            
        re_srch = re.search(rx_cv, line, flags=0)
        if re_srch:
            tsai_params.cv = float(re_srch.group('cv'))        
    
        re_srch = re.search(rx_k1, line, flags=0)
        if re_srch:
            tsai_params.k1 = float(re_srch.group('k1'))    
            
        re_srch = re.search(rx_k2, line, flags=0)
        if re_srch:
            tsai_params.k2 = float(re_srch.group('k2'))        
    
        re_srch = re.search(rx_p1, line, flags=0)
        if re_srch:
            tsai_params.p1 = float(re_srch.group('p1'))    
            
        re_srch = re.search(rx_p2, line, flags=0)
        if re_srch:
            tsai_params.p2 = float(re_srch.group('p2'))        
    
        re_srch = re.search(rx_pitch, line, flags=0)
        if re_srch:
            tsai_params.pitch = float(re_srch.group('pitch'))
        
    return tsai_params

#%% run module/function as script 

if __name__ == '__main__':
    
    import os
    # set input directory with ASP Tsai camera calibration file for parsing
    f_dir_cal = r".." + os.sep + "data" + os.sep + "calibration"
    # set Tsai input file name for parsing
    f_name = f_dir_cal + os.sep + "CAMBOT_28mm_51500462_ASP_cal_pix_mod.tsai"

    # execute function    
    tsai_params_asp = parse_asp_tsai_file(f_name)
    
    # Prosilica GT 4905C camera pixel size is 5.5 μm × 5.5 μm
    pixel_mm = 5.5 * 0.001
    
    # display some example values. center section headlines nicely
    horz_line = '-----------------------------------------------------------------'
    len_horz_line = len(horz_line)
    
    str_title = 'Prosilica GT 4905C camera with Zeiss 28 mm/F2 lens (S/N 51500462)'
    str_title = str_title.center(len_horz_line, " ")
    str_focal = 'Focal length estimates'
    str_focal = str_focal.center(len_horz_line, " ")
       
    str_principal = 'Center/principal point estimates'
    str_principal = str_principal.center(len_horz_line, " ")

    print(str_title)
    print(str_focal)
    print(horz_line)
    print(f'fu = {tsai_params_asp.fu*pixel_mm:5.2f} mm')
    print(f'fv = {tsai_params_asp.fv*pixel_mm:5.2f} mm\n')
    print(str_principal)
    print(horz_line)
    print(f'cu = {tsai_params_asp.cu:7.2f} pixels')
    print(f'cv = {tsai_params_asp.cv:7.2f} pixels')