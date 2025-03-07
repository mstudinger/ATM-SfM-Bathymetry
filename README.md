![repository_banner](presentations/supraglacial_lake_banner_image.jpg)  
# <div align="center">Bathymetry of supraglacial lakes and streams on the Greenland Ice Sheet from high-resolution aerial photography</div>
This repository contains tools for deriving supraglacial lake bathymetry from NASA's Airborne Topographic Mapper (ATM) aerial imagery using NASA's Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)), a suite of free and open source, automated geodesy and stereogrammetry tools. The repository is comprised of Jupyter notebooks, Python™ code and data files with the intention of publicly sharing tools and results as the project evolves. It is a living repository intended to invite people to contribute and comment and use the tools that are being developed.

>[!NOTE]
>* **Surface Topography and Vegetation (STV) Community Meeting at NASA GSFC, October 2024:** [Poster](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/presentations/STV_Community_Meeting_GSFC_2024_Greenland_lake_bathymetry.svgz.pdf)  
>* **Poster presentation at AGU's Annual Meeting 2024** in Washington, DC.: [Poster](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/presentations/AGU_Fall_Meeting_2024_Greenland_lake_bathymetry_poster_medium_res.pdf) [Linkt to AGU abstract](https://agu.confex.com/agu/agu24/meetingapp.cgi/Paper/1528333)  


**Jupyter notebooks currently available in this repository (more to come):**  
* **Tutorial:** [Step 1: Automatic detection of supraglacial lakes and surface classification](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_lake_detection_using_NDWI_and_Otsu_thresholding.ipynb) using classic image segmentation methods such as [Otsu](https://doi.org/10.1109/TSMC.1979.4310076) multi-thresholding and Connected Component Analysis (CCA) on both natural-color imagery and NDWI<sub>ice</sub>.  
* **Tutorial:** [Step 2: Automatic detection of supraglacial lakes](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOT_v2_lake_detection_using_SAM.ipynb) using the AI-based Segment Anything Model (SAM) ([Kirillov, A. et al., 2023](http://arxiv.org/abs/2304.02643)).  
* **Tutorial:** [Conversion of CAMBOTv2 L0 natural-color (RGB) images](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_RGB_to_luminance.ipynb) to single-channel grayscale (luminance) images for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)). The tutorial covers different ways of converting RGB to luminance.
* **Tutorial:** [Known challenges for SfM for supraglacial hydrology](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/SfM_supraglacial_hydrology_known_challenges.ipynb): Notebook illustrating known challenges for SfM for supraglacial hydrology, such as caustic and lake ice cover.  
* **Tool:** [Conversion of CAMBOTv2 GPS antenna positions](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_convert_GPS_to_camera_pos.ipynb) to the camera's focal plane position for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* **Tool:** [Parse ASP camera calibration files using the TSAI distortion model](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/parse_ASP_Tsai_camera_calibration_files.ipynb) and extract focal lengths $f_{u, v}$ as well as radial ($k_{1, 2}$) and tangential ($p_{1, 2}$) lens distortion parameters (see: [ASP frame camera models](https://stereopipeline.readthedocs.io/en/latest/pinholemodels.html)).
* **Tool:** [Toolbox](https://github.com/lidar532/ww_MetaShapelib) for converting commonly used Metashape lens calibration formats to NASA's Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)) Tsai format with tools for analysing a large number of Metashape error statics etc. The toolbox, written by [C. Wayne Wright](https://github.com/lidar532), contains an NBDEV enabled Jupyter notebook, a Python™ library module, and a pip package installer. It runs (and has been tested) in Google Colab, Windows, and Linux/WSL2.
* **Tutorial:** [Sample raster data along a profile](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/create_profile_sample_raster_tutorial.ipynb): Notebook demonstrating how to create a profile from start and end coordinates and sample raster values along the profile.   
***
**Python™ code currently available in this repository (more to come):**
* [Parse ASP camera calibration files using the TSAI distortion model](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/parse_ASP_TSAI_camera_calibration_files.py) and extract intrinsic parameters, such as focal lengths $f_{u, v}$ , radial ($k_{1, 2, 3}$) and tangential  lens distortion parameters ($p_{1, 2}$) , as well as extrinsic parameters such as camera pose (see: [ASP frame camera models](https://stereopipeline.readthedocs.io/en/latest/pinholemodels.html)).
* [Convert ASP residual output files to GeoPackage (GPKG) for plotting with GIS packages](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/convert_asp_residual_output_to_gpkg.py)
* [Convert ATM HDF5 lidar point clouds](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/convert_ATM_H5_to_csv_and_gpkd.py): convert ATM HDF5 lidar point clouds to ASCII CSV or GeoPackage (GPKG) for plotting with GIS packages.
* [Convert KT19 surface temperature measurements](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/convert_KT19_to_gpkg.py): convert KT19 surface temperature measurements to GeoDataFrame and save as GeoPackage (GPKG).
* [Calculate the index of refraction of water depending on temperature, wavelength, and salinity](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/calc_refractive_index_of_water.py) using [Christopher Parrish's (2020) empirical model](https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature)
* [Calculate NDWI<sub>ice</sub> from L1B georeferenced GeoTiff files and save NDWI<sub>ice</sub> as GeoTiff](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/calculate_L1B_NDWI_geotiffs.py)
***
**Notebooks and repositories related to this project:**  
[Lidar review tools](https://lidar532.github.io/lidar_review_tools/) from [C. Wayne Wright](https://github.com/lidar532) using ATM supraglacial lake data as example:
* [Lake surface detection](https://lidar532.github.io/lidar_review_tools/detect_lidar_water_surface.html)
* [Interactive Bokeh plots of lake surface](https://lidar532.github.io/lidar_review_tools/ww_bokeh.html)
___

**Recommended resources:**
* [Ames Stereo Pipeline user manual](https://stereopipeline.readthedocs.io/en/latest/index.html)
* [Ames Stereo Pipeline user group & support forum](https://groups.google.com/forum/#!forum/ames-stereo-pipeline-support)
* [Ames Stereo Pipeline daily build](https://github.com/NeoGeographyToolkit/StereoPipeline/releases)
* [Jupyter-ready docker image with ASP pre-installed](https://github.com/uw-cryo/asp-binder) from the [University of Washington Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)
* [Ames Stereo Pipeline tutorials](https://github.com/uw-cryo/asp_tutorials) from the [University of Washington Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)
*  [Christopher Parrish's (2020) empirical model for calculating the refractive index of water](https://research.engr.oregonstate.edu/parrish/index-refraction-seawater-and-freshwater-function-wavelength-and-temperature)

***

**Publications relevant to the Structure from Motion (SfM) Bathymetry repository:**
* Beyer, R. A., Alexandrov, O., and McMichael, S.: The Ames Stereo Pipeline: NASA’s Open Source Software for Deriving and Processing Terrain Data, Earth and Space Science, 5, 537–548, https://doi.org/10.1029/2018EA000409, 2018.
* Harpold, R., Yungel, J., Linkswiler, M., and Studinger, M.: Intra-scan intersection method for the determination of pointing biases of an airborne altimeter, International Journal of Remote Sensing, 37, 648–668, https://doi.org/10.1080/01431161.2015.1137989, 2016.
* Otsu, N.: A Threshold Selection Method from Gray-Level Histograms, IEEE Trans. Syst., Man, Cybern., 9, 62–66, https://doi.org/10.1109/TSMC.1979.4310076, 1979.
* Palaseanu-Lovejoy, M., Alexandrov, O., Danielson, J., and Storlazzi, C.: SaTSeaD: Satellite Triangulated Sea Depth Open-Source Bathymetry Module for NASA Ames Stereo Pipeline, Remote Sensing, 15, 3950, https://doi.org/10.3390/rs15163950, 2023.
* Shean, D. E., Alexandrov, O., Moratto, Z. M., Smith, B. E., Joughin, I. R., Porter, C., and Morin, P.: An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very-high-resolution commercial stereo satellite imagery, ISPRS Journal of Photogrammetry and Remote Sensing, 116, 101–117, https://doi.org/10.1016/j.isprsjprs.2016.03.012, 2016.
* Slocum, R. K., Wright, W., and Parrish, C.: Guidelines for Bathymetric Mapping and Orthoimage Generation using sUAS and SfM, An Approach for Conducting Nearshore Coastal Mapping, https://doi.org/10.25923/07MX-1F93, 2019.
* Studinger, M., Manizade, S. S., Linkswiler, M. A., and Yungel, J. K.: High-resolution imaging of supraglacial hydrological features on the Greenland Ice Sheet with NASA’s Airborne Topographic Mapper (ATM) instrument suite, The Cryosphere, 16, 3649–3668, https://doi.org/10.5194/tc-16-3649-2022, 2022.
* Yang, K. and Smith, L. C.: Internally drained catchments dominate supraglacial hydrology of the southwest Greenland Ice Sheet: Greenland Internally Drained Catchment, J. Geophys. Res. Earth Surf., 121, 1891–1910, https://doi.org/10.1002/2016JF003927, 2016.

