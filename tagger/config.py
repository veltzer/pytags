from __future__ import print_function
import imp
import os

imp.load_source('tagger.config','cfg.py')
overridefiles=os.path.expanduser('~/.cfg.py')
if os.path.isfile(overridefiles):
	imp.load_source('tagger.config',overridefiles)

def show():
	for ns_name in pdmt.config.__dict__:
		if ns_name.startswith('ns_'):
			print(ns_name)
			ns=pdmt.config.__dict__[ns_name]
			for p in ns.__dict__:
				print('\t',p,ns.__dict__[p])
