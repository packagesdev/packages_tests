#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the auth option is set to root for the package during the build process

test_displayed_name="distribution > packages > settings > options > require admin password - yes"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_packages_settings_options_require-admin-password.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_auth="root"

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)

tree=ET.parse(os.path.join(extraction_directory,'package.pkg','PackageInfo'))

root = tree.getroot()

auth = root.attrib['auth']

if (expected_auth == auth):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
    print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
    print("    Expected: '{}' ; Found: \033[91m'{}'\033[0m".format(expected_auth,auth))



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
