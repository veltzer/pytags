import argparse
import sys
import pytags.config

# see documentation in http://docs.python.org/library/argparse.html
opts = [
    "showconfig",
    "testconnect",
    "createdb",
    "scan",
    "search",
    "taglist",
    "raiseexception",
    "insertdir",
    "inserttag",
    "clean",
]


def parse(mgr):
    debug = False
    parser = argparse.ArgumentParser(description=pytags.config.ns_product["p_description"])
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
        '--createdb',
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
    parser.add_argument(
        '--search',
        help='search for a tag or tags in a folder',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--taglist',
        help='list all tags know to tagger',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--raiseexception',
        help='raise an exception (for testing purposes)',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--insertdir',
        help='insert a directory into the database (for testing purposes)',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--inserttag',
        help='insert a tag into the database (for testing purposes)',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--clean',
        help='clean the database (must pass --force)',
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
    options = parser.parse_args()
    if debug:
        print(options)
        sys.exit(1)
    if sum([
        options.showconfig,
        options.testconnect,
        options.createdb,
        options.scan,
        options.search,
        options.taglist,
        options.raiseexception,
        options.insertdir,
        options.inserttag,
        options.clean,
    ]) != 1:
        parser.error(f"must specify one of {','.join(opts)}")
    # pass flags
    pytags.config.ns_op.p_force = options.force
    pytags.config.ns_mgr.p_dir = options.dir
    # run the ops...
    if options.showconfig:
        mgr.showconfig()
    if options.testconnect:
        mgr.testconnect()
    if options.createdb:
        mgr.createdb()
    if options.scan:
        mgr.scan()
    if options.search:
        mgr.search()
    if options.taglist:
        mgr.taglist()
    if options.raiseexception:
        mgr.raiseexception()
    if options.insertdir:
        mgr.insertdir()
    if options.inserttag:
        mgr.inserttag()
    if options.clean:
        mgr.clean()
