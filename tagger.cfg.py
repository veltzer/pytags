# do not import any pdmt classes here except boot
# you may use other classes as long as they are supported in all versions
# of python you will be using
import tagger.utils.boot

class ns_product:
	# general info about the tagger product
	p_name='tagger'
	#p_version=tagger.utils.boot.system_check_output(['git','describe']).rstrip()
	p_version=0.1
	p_description='Tagger tagging wizard / Mark Veltzer'
class ns_db:
	# db connection details (don't put passwords here, put them in ~/.tagger.cfg.py instead)
	p_host='localhost'
	p_port=3306
	p_user='[YOUR USER]'
	p_password='[YOUR PASSWORD]'
	p_db='tagger'
class ns_op:
	# should we force things?
	p_force=False
class ns_mgr:
	# should we suppress warnings from mysql?
	p_suppress_warnings=True
	# which directory to scan?
	p_dir='.'
	# should we catch exceptions?
	p_catch=False
