Introduction
-------
Classify each pixel of an image as above or below a specified threshold value then convert the classified raster to a polygon representation.


Input
-------------
An input raster in GeoTiff format (*.tif).

Output
-------------
###### threshold.py
A classified raster in GeoTiff format (*.tif).
###### polygons.py
An polygon representation of the classified raster in shapefile format (*.shp).

Dependencies
--------------
<a href="www.numpy.org">numpy</a>, <a href="http://trac.osgeo.org/gdal/wiki/GdalOgrInPython">GDAL</a>


Examples
------------
There are two steps: 1) threshold an image with "threshold.py" and 2) convert the thresholded raster to a vector representation with "polygons.py". The two steps can be run as a pipeline using the driver ("driver.py"). 

_For the purpose of these examples, create a folder called output in the threshold directory._

##### Thresholding
The following examples classify each pixel of a canopy height model (with units in meters) as below 15.0 meters (classied as 1.0 or 1) and above 15.0 meters (classified at 0.0 or 0). The value after the -t flag represents the threshold value.

If running on UNIX-like system make sure permissions are set to executable.
`chmod u+x threshold.py`

Then run `./threshold.py -i chm_test.tif -o output/threshold15.0.tif -t 15.0 -v`

If using Windows, use the following:

`python threshold.py -i chm_test.tif -o output/threshold15.0.tif -t 15.0 -v`


##### Raster to Vector
Convert the classified raster from threshold.py into a vector representation (shapefile).

If running on UNIX-like system make sure permissions are set to executable.

`chmod u+x polygons.py`

Then run 

`./polygons.py -i output/threshold15.0.tif -o output/threshold15.0.shp -v`

If using Windows, use the following:

`python polygon.py -i output/threshold15.0.tif -o output/threshold15.0.shp -v`


##### Batch Mode
The script driver.py 1) provides batch like functionality to perform classification at a series of value thresholds and 2) serves as a pipeline to both threshold and convert from raster to vector. 

The example driver.cfg file will classify the chm_test.tif at all height thresholds between 2.0 m and 35.0 m using a step size of 1.0 (default). The output will be a series of files with the prefix threshold.

If running on UNIX-like system make sure permissions are set to executable.

`chmod u+x driver.py`

Then run 

`./driver.py -c driver.cfg -v`

If using Windows, use the following:

`python driver.py -c driver.cfg -v`



