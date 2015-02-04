#! /usr/bin/env python


"""
Polygons.py
"""

import gdal, ogr
from gdalconst import *
import argparse
from osgeo import osr

def getArgs():
	parser = argparse.ArgumentParser(
		description = "Convert raster to polygons"
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


def main():
	args = getArgs()

	if args.verbose:
		print args
	raster = gdal.Open(args.input, GA_ReadOnly)

	if args.band:
		band = raster.GetRasterBand(args.band)
	else:
		band = raster.GetRasterBand(1)

	driver = ogr.GetDriverByName("ESRI Shapefile")
	vector = driver.CreateDataSource(args.output)
	projection = osr.SpatialReference()
	projection.ImportFromWkt(raster.GetProjectionRef())
	layer = vector.CreateLayer("out", srs = projection)

	field = "class"
	field_def = ogr.FieldDefn(field, ogr.OFTInteger)
	layer.CreateField(field_def)
	field_type_example = 0

	maskband = None
	options = []
	output = gdal.Polygonize(band, maskband, layer, field_type_example, options)

	band = None
	raster = None
	shapefile = None


if __name__ == "__main__":
	main()