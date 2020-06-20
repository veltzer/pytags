import glob
import os
import subprocess

import config.general

# from user.personal import personal_slug

apt_protocol = "https"
apt_codename = subprocess.check_output(["lsb_release", "--codename", "--short"]).rstrip()
apt_arch = subprocess.check_output(
    "dpkg-architecture | grep -e ^DEB_BUILD_ARCH= | cut -d = -f 2", shell=True
).rstrip()
apt_architectures = "{0} source".format(apt_arch)
apt_component = "main"
apt_folder = "apt"
apt_service_dir = os.path.join(
    config.general.general_homedir, "public_html/public", apt_folder
)
# apt_except = '50{0}'.format(personal_slug)
apt_pack_list = glob.glob(
    os.path.join(config.general.general_homedir, "packages", "*.deb")
)
apt_pack_str = " ".join(apt_pack_list)
apt_id = subprocess.check_output(["lsb_release", "--id", "--short"]).rstrip()
apt_key_file = "public_key.gpg"
# apt_apache_site_file = '{0}.apt'.format(personal_slug)
