# this is wrong for the tag since they may not be alphabetically ordered...
# tag=subprocess.check_output(['git', 'tag']).decode().rstrip()
# if tag!='':
#    d.git_last_tag=tag.split()[-1].rstrip()
# else:
#    d.git_last_tag='no git tag yet'

# this is right
import subprocess

from config.helpers import help_check_output

git_last_tag = help_check_output(['git', 'describe', '--abbrev=0', '--tags'],
                                 stderr=subprocess.DEVNULL).rstrip()
git_describe = help_check_output(['git', 'describe'], stderr=subprocess.DEVNULL).rstrip()
git_version = '.'.join(git_describe.split('-'))
