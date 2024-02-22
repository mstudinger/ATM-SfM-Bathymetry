# Structure from Motion (SfM) Bathymetry
This repository contains tools for deriving supraglacial lake bathymetry from NASA's Airborne Topographic Mapper (ATM) aerial imagery using NASA's Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)), a suite of free and open source, automated geodesy and stereogrammetry tools. The repository is comprised of Jupyter notebooks, Python™ code and data files with the intention of publicly sharing tools and results as the project evolves. It is a living repository intended to invite people to contribute and comment and use the tools that are being developed.

__*The repository is within the spirit of NASA's Transform to Open Science ([TOPS](https://nasa.github.io/Transform-to-Open-Science/)) initiative with the goal of transforming communities to an inclusive culture of open science.*__

**Jupyter notebooks currently available in this repository (more to come):**
* [Conversion of CAMBOTv2 L0 natural-color (RGB) images](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_RGB_to_luminance.ipynb) to single-channel grayscale (luminance) images for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* [Conversion of CAMBOTv2 GPS antenna positions](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_convert_GPS_to_camera_pos.ipynb) to the camera's focal plane position for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* [Surface classification of supraglacial lakes](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_lake_detection_using_NDWI_and_Otsu_thresholding.ipynb) using surface classification based on natural-color imagery, NDWI<sub>ice</sub> and [Otsu](https://doi.org/10.1109/TSMC.1979.4310076) thresholding
* [Parse ASP camera calibration files using the TSAI distortion model](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/parse_ASP_Tsai_camera_calibration_files.ipynb) and extract focal lengths $f_{u, v}$ as well as radial ($k_{1, 2}$) and tangential ($p_{1, 2}$) lens distortion parameters (see: [ASP frame camera models](https://stereopipeline.readthedocs.io/en/latest/pinholemodels.html)).

**Python™ code currently available in this repository (more to come):**
* [Parse ASP camera calibration files using the TSAI distortion model](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Python/parse_ASP_TSAI_camera_calibration_files.py) and extract focal lengths $f_{u, v}$ as well as radial ($k_{1, 2}$) and tangential ($p_{1, 2}$) lens distortion parameters (see: [ASP frame camera models](https://stereopipeline.readthedocs.io/en/latest/pinholemodels.html)).

___

**Recommended resources:**
* [Ames Stereo Pipeline user manual](https://stereopipeline.readthedocs.io/en/latest/index.html)
* [Ames Stereo Pipeline user group & support forum](https://groups.google.com/forum/#!forum/ames-stereo-pipeline-support)
* [Jupyter-ready docker image with ASP pre-installed](https://github.com/uw-cryo/asp-binder) from the [University of Washington Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)
* [Ames Stereo Pipeline tutorials](https://github.com/uw-cryo/asp_tutorials) from the [University of Washington Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)

**Publications relevant to the Structure from Motion (SfM) Bathymetry repository:**
* Beyer, R. A., Alexandrov, O., and McMichael, S.: The Ames Stereo Pipeline: NASA’s Open Source Software for Deriving and Processing Terrain Data, Earth and Space Science, 5, 537–548, https://doi.org/10.1029/2018EA000409, 2018.
* Harpold, R., Yungel, J., Linkswiler, M., and Studinger, M.: Intra-scan intersection method for the determination of pointing biases of an airborne altimeter, International Journal of Remote Sensing, 37, 648–668, https://doi.org/10.1080/01431161.2015.1137989, 2016.
* Otsu, N.: A Threshold Selection Method from Gray-Level Histograms, IEEE Trans. Syst., Man, Cybern., 9, 62–66, https://doi.org/10.1109/TSMC.1979.4310076, 1979.
* Palaseanu-Lovejoy, M., Alexandrov, O., Danielson, J., and Storlazzi, C.: SaTSeaD: Satellite Triangulated Sea Depth Open-Source Bathymetry Module for NASA Ames Stereo Pipeline, Remote Sensing, 15, 3950, https://doi.org/10.3390/rs15163950, 2023.
* Shean, D. E., Alexandrov, O., Moratto, Z. M., Smith, B. E., Joughin, I. R., Porter, C., and Morin, P.: An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very-high-resolution commercial stereo satellite imagery, ISPRS Journal of Photogrammetry and Remote Sensing, 116, 101–117, https://doi.org/10.1016/j.isprsjprs.2016.03.012, 2016.
* Slocum, R. K., Wright, W., and Parrish, C.: Guidelines for Bathymetric Mapping and Orthoimage Generation using sUAS and SfM, An Approach for Conducting Nearshore Coastal Mapping, https://doi.org/10.25923/07MX-1F93, 2019.
* Studinger, M., Manizade, S. S., Linkswiler, M. A., and Yungel, J. K.: High-resolution imaging of supraglacial hydrological features on the Greenland Ice Sheet with NASA’s Airborne Topographic Mapper (ATM) instrument suite, The Cryosphere, 16, 3649–3668, https://doi.org/10.5194/tc-16-3649-2022, 2022.
* Yang, K. and Smith, L. C.: Internally drained catchments dominate supraglacial hydrology of the southwest Greenland Ice Sheet: Greenland Internally Drained Catchment, J. Geophys. Res. Earth Surf., 121, 1891–1910, https://doi.org/10.1002/2016JF003927, 2016.

