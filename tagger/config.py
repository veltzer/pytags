from __future__ import print_function
import imp
import os

imp.load_source('tagger.config','tagger.cfg.py')
overridefiles=os.path.expanduser('~/.tagger.cfg.py')
if os.path.isfile(overridefiles):
	imp.load_source('tagger.config',overridefiles)

def show():
	for ns_name in tagger.config.__dict__:
		if ns_name.startswith('ns_'):
			print(ns_name)
			ns=tagger.config.__dict__[ns_name]
			for p in ns.__dict__:
				if p.startswith('p_'):
					print('\t',p,ns.__dict__[p])
