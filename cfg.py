# do not import any pdmt classes here except boot
# you may use other classes as long as they are supported in all versions
# of python you will be using
import tagger.utils.boot

class ns_tagger:
	p_version=tagger.utils.boot.system_check_output(['git','describe']).rstrip()
class ns_product:
	p_name='tagger'
	p_version=tagger.utils.boot.system_check_output(['git','describe']).rstrip()
	p_description='Project Dependency Management Tool'
class ns_db:
	p_name='tagger'
	p_user='mark'
	p_password='';
