# -*- coding: utf-8 -*-
"""
Created on Mon Dec 4, 2023
Revised on Thu May 2, 2024

Simple Python script for calculating the index of refraction using the empirical model from Christopher Parrish (2020):
https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature
and Richie Slocum:
https://github.com/hokiespurs/water_ior
and references therein  

@author: Michael Studiner, NASA Goddard Space Flight Center
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

