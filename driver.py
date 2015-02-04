#! /usr/bin/env python


"""
Driver for threshold.py
"""
import argparse, ConfigParser, shlex, time, os
import subprocess as sp
import numpy as np

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
		lengths=dict(config.items("height"))
		print lengths
		l_str=lengths["height"]
		print l_str
		if ("," in l_str) and (":" in l_str):
			raise Exception
		elif "," in l_str:
			l_list = l_str.split(",")
			l_list = [float(L) for L in l_list]
			l_list = np.array(l_list)
		elif ":" in l_str:
			l_range = l_str.split(":")
			l_range = [float(L) for L in l_range]
			if len(l_range)==2:
				l_min, l_max = l_range[0],l_range[1] + 1
				l_list = np.arange(l_min, l_max, 1.0)
			elif len(l_range)==3:
				l_min, l_max, step = l_range[0],l_range[1] + 1, l_range[2]
				l_list = np.arange(l_min, l_max, step)
			else:
				print "Problem with height configuration."
				raise e
		else:
			l_list = np.array([float(l_str)])
		Configs["height"] = l_list
	except Exception as e:
		print "Problem parsing configuration file {}. Check file.".format(configFile)
		raise e
	return Configs

def driver(configs, args):
	for h in configs["height"]:
		if args.verbose:
			cmd = "python {} -i {} -o {} -t {} -v".format(
				configs["path"]["threshold"],
				configs["path"]["chm"],
				configs["path"]["output"],
				h
			)
			print cmd
		else:
			cmd = "python {} -i {} -o {} -t {}".format(
				configs["path"]["threshold"],
				configs["path"]["dem"],
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

def main():
	t_i = time.time()
	args = getArgs()
	configs = getConfigs(args.config)
	driver(configs, args)
	t_f = time.time()
	if args.verbose:
		print "Total elapsed time was {} minutes".format((t_f-t_i)/60.)

if __name__ == "__main__":
	main()
