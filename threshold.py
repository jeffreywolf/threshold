#! /usr/bin/env python


"""
Threshold image
"""

import gdal
from gdalconst import *
import numpy as np
import argparse
from osgeo import osr

def getArgs():
	parser = argparse.ArgumentParser(
		description = "Threshold an image. Values above the \
threshold are coded as 0 and below as 1."
	)

	parser.add_argument(
		"-i",
		"--input",
		type = str,
		required = True,
		help = "input raster file"
	)

	parser.add_argument(
		"-b",
		"--band",
		type = str,
		required = False,
		help = "Band (indexing starts at 1). Default is band 1."
	)

	parser.add_argument(
		"-t",
		"--threshold",
		type = str,
		required = True,
		help = "Threshold value."
	)	

	parser.add_argument(
		"-o",
		"--output",
		type = str,
		required = True,
		help = "Output file name"
	)

	parser.add_argument(
		"-v",
		"--verbose",
		action = "store_true",
		help = "Print status updates while executing"
	)

	return parser.parse_args()

def getGeoInfo(filename):
	raster = gdal.Open(filename, GA_ReadOnly)
	NDV = raster.GetRasterBand(1).GetNoDataValue()
	xsize = raster.GetRasterBand(1).XSize
	ysize = raster.GetRasterBand(1).YSize
	GeoT = raster.GetGeoTransform()
	Projection = osr.SpatialReference()
	Projection.ImportFromWkt(raster.GetProjectionRef())
	DataType = raster.GetRasterBand(1).DataType
	DataType = gdal.GetDataTypeName(DataType)
	return NDV, xsize, ysize, GeoT, Projection, DataType

def createGTiff(Name, Array, driver, NDV,
				xsize, ysize, GeoT, Projection, DataType, band = 1):
	if DataType == "Float32":
		DataType = gdal.GDT_Float32
	# set nans to original no data value
	Array[np.isnan(Array)] = NDV
	# Set data
	band = 1
	DataSet = driver.Create(Name, xsize, ysize, band, DataType)
	DataSet.SetGeoTransform(GeoT)
	DataSet.SetProjection(Projection.ExportToWkt())
	# Write array
	DataSet.GetRasterBand(1).WriteArray(Array)
	DataSet.GetRasterBand(1).SetNoDataValue(NDV)
	# Close DataSet
	DataSet = None
	return Name



def main():
	args = getArgs()

	if args.verbose:
		print args
	raster = gdal.Open(args.input)
	NDV, xsize, ysize, GeoT, Projection, DataType = getGeoInfo(args.input)

	if args.band:
		band = raster.GetRasterBand(args.band)
	else:
		band = raster.GetRasterBand(1)

	array = band.ReadAsArray()
	#output_array = np.zeros(array.shape, array.dtype)+400+array
	output_array = np.zeros(array.shape, array.dtype)
	output_array[array == NDV] = np.nan

	output_array[array!=NDV] = array[array!=NDV] <= float(args.threshold)

	if args.verbose:
		print output_array
	driver = gdal.GetDriverByName('GTiff')
	new_filename = createGTiff(args.output, output_array, driver, NDV, 
								xsize, ysize, GeoT, Projection, DataType)


if __name__ == "__main__":
	main()