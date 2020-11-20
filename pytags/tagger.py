#!/usr/bin/python

import pytags.cmdline
import pytags.mgr
import tagger.config

def work():
    mgr=tagger.mgr.Mgr()
    tagger.cmdline.parse(mgr)

def main():
    if tagger.config.ns_mgr.p_catch:
        try:
            work()
        except Exception as e:
            print(e)
    else:
        work()


if __name__ == "__main__":
    main()
