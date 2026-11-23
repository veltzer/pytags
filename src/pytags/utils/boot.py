"""
This is a module which should never use pdmt classes. It is intended to aid in the
writing of the pdmt config

It intentionaly will duplicate code in other utils since it is a boot strapper.
"""

import os


def dir_list(arg):
    return [x[0] for x in os.walk(arg)]
