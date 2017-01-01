#!/usr/bin/python

import tagger.cmdline
import tagger.mgr
import tagger.config

def work():
    mgr=tagger.mgr.Mgr()
    tagger.cmdline.parse(mgr)

def main():
    if tagger.config.ns_mgr.p_catch:
        try:
            work()
        except Exception,e:
            print e
    else:
        work()


if __name__ == "__main__":
    main()
