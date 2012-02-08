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
	parser.add_argument(
			'--build',
			help='build project',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--printgraph',
			help='print the graph (may be long)',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--dotgraph',
			help='write the graph to a .dot file',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--showops',
			help='dump operations',
			action='store_true',
			default=False,
	)
	parser.add_argument(
			'--runop',
			metavar='operation',
			help='run an operation',
			action='store',
			default=None,
	)
	options=parser.parse_args()
	if debug:
		print(options)
		sys.exit(1)
	runop_int=0
	if options.runop is not None:
		runop_int=1
	if sum([
		options.clean,
		options.build,
		options.printgraph,
		options.dotgraph,
		options.showops,
		options.showconfig,
		runop_int,
	])!=1:
		parser.error('must specify one of clean,build,printgraph,dotgraph,showops,showconfig,runop')
	if options.clean:
		mgr.clean()
	if options.build:
		mgr.build()
	if options.printgraph:
		mgr.printgraph()
	if options.dotgraph:
		mgr.dotgraph()
	if options.showops:
		print('here is the list');
		for x in mgr.getOperations():
			print('\t',x)
	if options.showconfig:
		pdmt.config.show()
	if options.runop:
		if mgr.hasOperation(options.runop):
			mgr.runOperation(options.runop)
		else:
			print('no such operation',options.runop);
			print('here is the list');
			for x in mgr.getOperations():
				print('\t',x)
