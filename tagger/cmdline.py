from __future__ import print_function
import argparse
import sys
import tagger.config

# see documentation in http://docs.python.org/library/argparse.html

def parse(mgr):
	debug=False
	parser=argparse.ArgumentParser(description=tagger.config.ns_product.p_description)
	parser.add_argument(
			'--showconfig',
			help='show the config (after processing)',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--create',
			help='create the database',
			action='store_true',
			default=False,
	)
	options=parser.parse_args()
	if debug:
		print(options)
		sys.exit(1)
	if sum([
		options.showconfig,
		options.create,
	])!=1:
		parser.error('must specify one of clean,build,printgraph,dotgraph,showops,showconfig,runop')
	if options.showconfig:
		mgr.showconfig()
	if options.create:
		mgr.create()
