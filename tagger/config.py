from __future__ import print_function
import imp
import os

home_config='~/.tagger.cfg.py'
dir_config='tagger.cfg.py'
imp.load_source('tagger.config',dir_config)
overridefiles=os.path.expanduser(home_config)
if os.path.isfile(overridefiles):
    imp.load_source('tagger.config',overridefiles)

def show():
    print('reading config from',dir_config,',',home_config)
    for ns_name in tagger.config.__dict__:
        if ns_name.startswith('ns_'):
            print(ns_name)
            ns=tagger.config.__dict__[ns_name]
            for p in ns.__dict__:
                if p.startswith('p_'):
                    print('\t',p,ns.__dict__[p])
