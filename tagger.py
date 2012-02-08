#!/usr/bin/python


import tagger.cmdline
import tagger.mgr

mgr=tagger.mgr.Mgr()
tagger.cmdline.parse(mgr)
