#! /usr/bin/env python


"""
Driver for threshold.py
"""
import argparse, ConfigParser, shlex, time, os, itertools
import subprocess as sp
import numpy as np
import multiprocessing as mp

def getArgs():
	parser = argparse.ArgumentParser(
		description = "Driver for threshold.py"
	)
	parser.add_argument(
		"-c",
		"--config",
		required = True,
		help = "location of a configuration file"
	)
	parser.add_argument(
		"-v",
		"--verbose",
		action = "store_true",
		help = "Print status while executing"
	)
	return parser.parse_args()

def getConfigs(configFile):
	Configs = {}
	try:
		config = ConfigParser.ConfigParser()
		config.read(configFile)
		Configs["path"] = dict(config.items("path"))
		print Configs
		height=dict(config.items("height"))
		print height
		h_str=height["height"]
		print h_str
		if ("," in h_str) and (":" in h_str):
			raise Exception
		elif "," in h_str:
			h_list = h_str.split(",")
			h_list = [int(L) for L in h_list]
			h_list = np.array(h_list)
		elif ":" in h_str:
			h_range = h_str.split(":")
			h_range = [int(L) for L in h_range]
			if len(h_range)==2:
				h_min, h_max = h_range[0],h_range[1] + 1
				h_list = range(h_min, h_max)
			elif len(h_range)==3:
				h_min, h_max, step = h_range[0],h_range[1] + 1, h_range[2]
				h_list = range(h_min, h_max, step)
			else:
				print "Problem with height configuration."
				raise e
		else:
			h_list = np.array([int(h_str)])
		Configs["height"] = h_list
	except Exception as e:
		print "Problem parsing configuration file {}. Check file.".format(configFile)
		raise e
	return Configs

def threshold(configs, args):
	for h in configs["height"]:
		if args.verbose:
			cmd = "python {} -i {} -o {}/threshold{}.tif -t {} -v".format(
				configs["path"]["threshold"],
				configs["path"]["chm"],
				configs["path"]["output"],
				h,
				h
			)
			print cmd
		else:
			cmd = "python {} -i {} -o {}/threshold{}.tif -t {}".format(
				configs["path"]["threshold"],
				configs["path"]["chm"],
				configs["path"]["output"],
				h,
				h
			)
		cmd_args = shlex.split(cmd)
		stdout,stderr = sp.Popen(
			cmd_args,
			stdin = sp.PIPE,
			stdout = sp.PIPE,
			stderr = sp.PIPE
		).communicate()
		if args.verbose:
			print stdout, stderr
	return True

def map_func(h, configs, args):
	"""Polygons command line in parallel.
	"""
	if args.verbose:
		cmd = "python {} -i {}/threshold{}.tif -o {}/threshold{}.shp -v".format(
			configs["path"]["polygons"],
			configs["path"]["output"],
			h,
			configs["path"]["output"],
			h
		)
		print cmd
	else:
		cmd = "python {} -i {}/threshold{}.tif -o {}/threshold{}.shp".format(
			configs["path"]["polygons"],
			configs["path"]["output"],
			h,
			configs["path"]["output"],
			h
		)
	cmd_args = shlex.split(cmd)
	stdout,stderr = sp.Popen(
		cmd_args,
		stdin = sp.PIPE,
		stdout = sp.PIPE,
		stderr = sp.PIPE
	).communicate()
	if args.verbose:
		print stdout, stderr
	return True

def map_star_func(a_b):
	return map_func(*a_b)

def main():
	t_i = time.time()
	args = getArgs()
	configs = getConfigs(args.config)
	threshold(configs, args)

	cores = mp.cpu_count()
	pool = mp.Pool(processes = cores)
	pool.map(
		map_star_func,
		itertools.izip(
			configs["height"],
			itertools.repeat(configs),
			itertools.repeat(args)
		)
	)

	t_f = time.time()
	if args.verbose:
		print "Total elapsed time was {} minutes".format((t_f-t_i)/60.)

if __name__ == "__main__":
	main()
