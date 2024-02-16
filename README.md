# Structure from Motion (SfM) Bathymetry
This repository contains tools for deriving supraglacial lake bathymetry from NASA's Airborne Topographic Mapper (ATM) aerial imagery using NASA's Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)), a suite of free and open source, automated geodesy and stereogrammetry tools. The repository is comprised of Jupyter notebooks, Python™ code and data files with the intention of publicly sharing tools and results as the project evolves. It is a living repository intended to invite people to contribute and comment and use the tools that are being developed. The repository is within the spirit of NASA's Transform to Open Science ([TOPS](https://nasa.github.io/Transform-to-Open-Science/)) initiative with the goal of transforming communities to an inclusive culture of open science.

**Jupyter notebooks:**
* [Conversion of CAMBOTv2 L0 natural-color (RGB) images](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_RGB_to_luminance.ipynb) to single-channel grayscale (luminance) images for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* [Conversion of CAMBOTv2 GPS antenna positions](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_convert_GPS_to_camera_pos.ipynb) to the camera's focal plane position for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* [Detection of supra-glacial lakes](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_lake_detection_using_NDWI_and_Otsu_thresholding.ipynb) using surface classification based on natural-color imagery, NDWI<sub>ice</sub> and Otsu thresholding

**Recommended resources:**
* [Ames Stereo Pipeline user manual](https://stereopipeline.readthedocs.io/en/latest/index.html)
* [Ames Stereo Pipeline user group & support forum](https://groups.google.com/forum/#!forum/ames-stereo-pipeline-support)
* [Jupyter-ready docker image with ASP pre-installed](https://github.com/uw-cryo/asp-binder) from the [UW Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)
* [Ames Stereo Pipeline tutorials](https://github.com/uw-cryo/asp_tutorials) from the [UW Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo) 
