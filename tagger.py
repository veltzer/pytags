#!/usr/bin/python

import tagger.cmdline
import tagger.mgr
import tagger.config

try:
	mgr=tagger.mgr.Mgr()
	tagger.cmdline.parse(mgr)
except Exception,e:
	if tagger.config.ns_mgr.p_catch:
		print e
	else:
		raise e
