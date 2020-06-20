import config.apt
from config.git import git_version

deb_version = '{0}~{1}'.format(git_version, config.apt.apt_codename)
