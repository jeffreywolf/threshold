README
======

General
-------
Classify each pixel of an image as above or below a specified threshold value. The output image will be the same data type as the input image.

Input
-------------
An input file -- tested with geoTiffs.

Output
-------------
An output file in geoTiff format (will have .tif extension).

Dependencies
--------------
GDAL, osr, numpy


Example call
------------
If running on UNIX-like system make sure permissions are set to executable.
`chmod u+x threshold.py`

The following examples classify each pixel of the input image as below 5 (classied as 1.0 or 1) and above 5 (classified at 0.0 or 0). The value after the -t flag represents the threshold value.

Then run `./threshold.py -i inputRaster.tif -o outputRaster.tif -t 5`

If using Windows, use the following:

`python meanFilter.py -i inputRaster.tif -o outputRaster.tif -t 5`

Where in all cases `inputRaster.tif` is the input raster name and `outputRaster.tif` is the name for the new mean filtered raster.

If the raster is multibanded, use the `-b` option to select the band to threshold.  This program processes a single band at a time. The default band is 1 (with indexing beginning at 1).

Notes
-------------
The i/o for this program is adapted from a Stack Exchange post by EddyTheB @ `http://gis.stackexchange.com/questions/57005/python-gdal-write-new-raster\
-using-projection-from-old`.