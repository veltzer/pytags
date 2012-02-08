from __future__ import print_function
import argparse
import sys
import tagger.config

# see documentation in http://docs.python.org/library/argparse.html

def parse(mgr):
	debug=False
	parser=argparse.ArgumentParser(description=tagger.config.ns_product.p_description)
	# major ops
	parser.add_argument(
			'--showconfig',
			help='show the config (after processing)',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--testconnect',
			help='test the connection to the database (no errors is good)',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--create',
			help='create the database (use --force to remove old)',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--scan',
			help='scan a folder recursivly (--dir to override folder)',
			action='store_true',
			default=False,
	)
	# variables overrides
	parser.add_argument(
			'--force',
			help='force doing things',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--dir',
			help='directory to scan',
			action='store',
			default='.',
	)
	options=parser.parse_args()
	if debug:
		print(options)
		sys.exit(1)
	if sum([
		options.showconfig,
		options.testconnect,
		options.create,
		options.scan,
	])!=1:
		parser.error('must specify one of showconfig,testconnect,create,scan')
	# pass flags
	tagger.config.ns_op.p_force=options.force
	tagger.config.ns_mgr.p_dir=options.dir
	# run the ops...
	if options.showconfig:
		mgr.showconfig()
	if options.testconnect:
		mgr.testconnect()
	if options.create:
		mgr.create()
	if options.scan:
		mgr.scan()
