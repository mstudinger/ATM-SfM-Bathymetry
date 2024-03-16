# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20, 2024.
Updated on Fri Mar 15, 2024 to include extrinsics.

@author: Michael Studinger, NASA - Goddard Space Flight Center
"""

# import required modules
import re

def parse_asp_tsai_file(
    f_name:str,   # ASP camera calibration file using the Tsai camera calibration technique
    ) -> object:  # a class containing the extracted parameters that were found

    """
      Parse ASP camera calibration file using the Tsai camera calibration technique,
      extract parameters, and return a class with the extracted values that were found.
      For a description of the ASP camera file formats see:
      https://stereopipeline.readthedocs.io/en/latest/pinholemodels.html#overview
    """
    
    # read camera/lens calibration file for parsing
    lens_cal = open(f_name, 'r')
    tsai_info = lens_cal.readlines() # reads the entire file
    lens_cal.close()
    
    # define a class TsaiParams for organizing the extracted lens calibration parameters
    class TsaiParams():
        def __init__(self):
            self.fu      = None # focal length in horizontal pixel units
            self.fv      = None # focal length in vertical pixel units
            self.cu      = None # horizontal offset of the principal point of the camera in the image plane in pixel units, from 0,0
            self.cv      = None # vertical offset of the principal point of the camera in the image plane in pixel units, from 0,0
            self.k1      = None # radial distortion parameter 1
            self.k2      = None # radial distortion parameter 2
            self.p1      = None # tangential distortion parameter 1
            self.p2      = None # tangential distortion parameter 2
            self.pitch   = None # the size of each pixel in pixles (1.l0) or millimeters or meters
            self.center  = None # location of the camera center, usually in the geocentric coordinate system (GCC/ECEF)
            self.rot_mat = None # rotation matrix describing the camera’s absolute pose in the coordinate system
    
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
    # location of camera center, usually in the geocentric coordinate system (GCC/ECEF)
    rx_center = r"C = (?P<x>-*\d+\.\d*) (?P<y>-*\d+\.\d+) *(?P<z>-*\d*\.\d*)"
    # rotation matrix describing the camera’s absolute pose in the coordinate system
    rx_rot_mat = r"R = (?P<m1>-*\d+\.\d*) (?P<m2>-*\d+\.\d+) *(?P<m3>-*\d*\.\d*) (?P<m4>-*\d+\.\d*) (?P<m5>-*\d+\.\d+) *(?P<m6>-*\d*\.\d*) (?P<m7>-*\d+\.\d*) (?P<m8>-*\d+\.\d+) *(?P<m9>-*\d*\.\d*)"
    
    
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
        
        re_srch = re.search(rx_center, line, flags=0)
        if re_srch:
            tsai_params.x = float(re_srch.group('x'))
            tsai_params.y = float(re_srch.group('y'))
            tsai_params.z = float(re_srch.group('z'))

        re_srch = re.search(rx_rot_mat, line, flags=0)
        if re_srch:            
            tsai_params.m1 = float(re_srch.group('m1'))
            tsai_params.m2 = float(re_srch.group('m2'))
            tsai_params.m3 = float(re_srch.group('m3'))
            tsai_params.m4 = float(re_srch.group('m4'))
            tsai_params.m5 = float(re_srch.group('m5'))
            tsai_params.m6 = float(re_srch.group('m6'))
            tsai_params.m7 = float(re_srch.group('m7'))
            tsai_params.m8 = float(re_srch.group('m8'))
            tsai_params.m9 = float(re_srch.group('m9'))        
        
    return tsai_params

#%% run module/function as script 

if __name__ == '__main__':
    
    import os
    # set input directory with ASP Tsai camera calibration file for parsing
    f_dir_cal = r".." + os.sep + "data" + os.sep + "calibration"
    # set Tsai input file name for parsing
    f_name = f_dir_cal + os.sep + "CAMBOT_28mm_51500462_ASP_cal_pix_mod.tsai"
    
    f_name = r"\\wsl.localhost\Ubuntu\home\mstuding\SfM\20190506\IOCAM0_2019_GR_NASA_20190506-131611.4217.tsai"


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