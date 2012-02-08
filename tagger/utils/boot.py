import subprocess
import os
"""
This is a module which should never use pdmt classes. It is intended to aid in the
writing of the pdmt config

It intentionaly will duplicate code in other utils since it is a boot strapper.
"""
# this function is here because of python2.6 that does not have subprocess.check_output
def system_check_output(arg):
	pr=subprocess.Popen(arg,stdout=subprocess.PIPE)
	(output,errout)=pr.communicate()
	status=pr.returncode
	if status:
		raise ValueError('error in executing',arg)
	return output
def dir_list(arg):
	p_dir_list=[]
	for x in os.walk(arg):
		p_dir_list.append(x[0])
	return p_dir_list
