#!/usr/bin/python

import tagger.cmdline
import tagger.mgr

#try:
mgr=tagger.mgr.Mgr()
tagger.cmdline.parse(mgr)
#except Exception,e:
#	print e
#	print e[1]
