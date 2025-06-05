# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4, 2023
Revised on Thu May  2, 2024
        on Tue Apr 29, 2025 added Dietrich and Parrish, 2025 (https://doi.org/10.1029/2024EA004106)

Simple Python script for calculating the index of refraction using the empirical model from Christopher Parrish (2020):
https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature
and Richie Slocum:
https://github.com/hokiespurs/water_ior
and references therein

April 29, 205: added Dietrich and Parrish, 2025 (https://doi.org/10.1029/2024EA004106)  

@author: Michael Studinger, NASA Goddard Space Flight Center
"""

import os

"""
    Index of Refraction of Seawater and Freshwater as a Function of Wavelength and Temperature
    Christopher Parrish (2020)
    
    https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature
    MATLAB and Python code on gitHub: https://github.com/hokiespurs/water_ior 
    The following empirical equation can be used to compute the index of refraction of saltwater or freshwater to 3-4 decimal places:
    n = aT^2 + bλ^2 + cT + dλ + e
    n = index of refraction
    T = temperature in °C (valid range: 0-30)
    λ = wavelength in nm (valid range 400-700 ~ visible spectrum)
    
"""

#%% set input parameters
 
WATER = 0         # 0 = freshwater, 1 = seawater
temp  = 0.0       # temperature in °C - valid range: 0-30
wavelength = 532  # wavelength  in nm - valid range: 400-700 (~ visible spectrum)

#%% check input parameters
if temp > 30 or temp < 0:
    os.sys.exit("The temperature in °C needs to be between 0°C and 30°C. Abort.")
    
if wavelength > 700 or wavelength < 400:
    os.sys.exit("The wavelength in nm needs to be between 400 nm and 700 nm. Abort.")    

#%% set coefficients

if WATER == 0:
    # freshwater constants
    a = -0.000001978124999
    b =  0.000000103223477
    c = -0.000008581249990
    d = -0.000154833692090
    e =  1.389193029374634
    water = "freshwater"
elif WATER == 1:
    # seawater constants
    a = -0.000001501562500
    b =  0.000000107084865
    c = -0.000042759374989
    d = -0.000160475520686
    e =  1.398067112092424
    water = "seawater"
else:
    os.sys.exit("WATER needs to be 0 (freshwater) or 1 (seawater). Abort.")

#%% calculate refractive index of water
    
ior = a*temp**2 + b*wavelength**2 + c*temp + d*wavelength + e

print(f'\n\tThe index of refraction of {water:s} at {temp:.1f}°C and {wavelength:d} nm is: {ior:.4f}')


#%% Dietrich and Parrish, 2025 (https://doi.org/10.1029/2024EA004106) 
# Development and Analysis of a Global Refractive Index of Water Data Layer for Spaceborne and Airborne Bathymetric Lidar

# 532 nm (equation 15) note: temperature range can be 0°C to 40°C here 
 
S = 0.1 # salinity in practical salinity units (PSU). Essentially, one PSU represents 1 gram of salt per 1000 grams of water fresh water 0.5

nw_532 = S * (1.6E-8 * temp**2 - 1.05E-6 * temp + 1.99611E-4) - 2.02E-6 * temp**2 - 7.95113E-6 * temp + 1.336

print(f'\n\tDietrich and Parrish 2025 for S = {S:.1f} PSU (practical salinity units)')
print(f'\tThe index of refraction of {water:s} at {temp:.1f}°C and {wavelength:d} nm is: {nw_532:.4f}')

