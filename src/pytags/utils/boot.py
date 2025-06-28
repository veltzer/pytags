"""
This is a module which should never use pdmt classes. It is intended to aid in the
writing of the pdmt config

It intentionaly will duplicate code in other utils since it is a boot strapper.
"""

import os


def dir_list(arg):
    p_dir_list = []
    for x in os.walk(arg):
        p_dir_list.append(x[0])
    return p_dir_list
