# Structure from Motion (SfM) Bathymetry
This repository contains tools for deriving supraglacial lake bathymetry from NASA's Airborne Topographic Mapper (ATM) aerial imagery using NASA's Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)), a suite of free and open source, automated geodesy and stereogrammetry tools. The repository is comprised of Jupyter notebooks, Python™ code and data files with the intention of publicly sharing tools and results as the project evolves. It is a living repository intended to invite people to contribute and comment and use the tools that are being developed. The repository is within the spirit of NASA's Transform to Open Science ([TOPS](https://nasa.github.io/Transform-to-Open-Science/)) initiative with the goal of transforming communities to an inclusive culture of open science.

**Jupyter notebooks currently available in this repository (more to come):**
* [Conversion of CAMBOTv2 L0 natural-color (RGB) images](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_RGB_to_luminance.ipynb) to single-channel grayscale (luminance) images for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* [Conversion of CAMBOTv2 GPS antenna positions](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_convert_GPS_to_camera_pos.ipynb) to the camera's focal plane position for use with the Ames Stereo Pipeline ([ASP](https://stereopipeline.readthedocs.io/en/latest/index.html)).
* [Detection of supra-glacial lakes](https://github.com/mstudinger/ATM-SfM-Bathymetry/blob/main/Jupyter/CAMBOTv2_lake_detection_using_NDWI_and_Otsu_thresholding.ipynb) using surface classification based on natural-color imagery, NDWI<sub>ice</sub> and Otsu thresholding

**Recommended resources:**
* [Ames Stereo Pipeline user manual](https://stereopipeline.readthedocs.io/en/latest/index.html)
* [Ames Stereo Pipeline user group & support forum](https://groups.google.com/forum/#!forum/ames-stereo-pipeline-support)
* [Jupyter-ready docker image with ASP pre-installed](https://github.com/uw-cryo/asp-binder) from the [University of Washington Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)
* [Ames Stereo Pipeline tutorials](https://github.com/uw-cryo/asp_tutorials) from the [University of Washington Terrain Analysis and Cryosphere Observation Lab](https://github.com/uw-cryo)

**Publications relevant to the Structure from Motion (SfM) Bathymetry repository:**
* Slocum R.K. *et al.*, (2019) [Guidelines for Bathymetric Mapping and Orthoimage Generation using sUAS and SfM, An Approach for Conducting Nearshore Coastal Mapping](https://repository.library.noaa.gov/view/noaa/22923)
* Beyer, R.A., Oleg Alexandrov, and Scott McMichael (2018). [The Ames Stereo Pipeline: NASA’s open source software for deriving and processing terrain data. Earth and Space Science, 5](https://doi.org/10.1029/2018EA000409).
* Shean, D.E., *et. al*, (2016). An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very high-resolution commercial stereo satellite imagery. [ISPRS Journal of Photogrammetry and Remote Sensing. 116](https://doi.org/10.1016/j.isprsjprs.2016.03.012).
* Palaseanu-Lovejoy, M. *et. al*, (2016), SaTSeaD: Satellite Triangulated Sea Depth Open-Source Bathymetry Module for NASA Ames Stereo Pipeline, [Remote Sensing](https://www.mdpi.com/2072-4292/15/16/3950)
* Studinger M., *et. al*, (2022), High-resolution imaging of supraglacial hydrological features on the Greenland Ice Sheet with NASA's Airborne Topographic Mapper (ATM) instrument suite, [The Cryosphere](https://doi.org/10.5194/tc-16-3649-2022)
* Harpold, R., Yungel, J., Linkswiler, M., and Studinger, M. (2016): Intra-scan intersection method for the determination of pointing biases of an airborne altimeter, [Int. J. Remote Sens., 37, 648–668](https://doi.org/10.1080/01431161.2015.1137989).  
