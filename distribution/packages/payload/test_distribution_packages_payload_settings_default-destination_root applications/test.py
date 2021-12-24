#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the install location  is set to /Applications in the settings during the build process

test_displayed_name="distribution > packages > payload > settings > default destination - /Applications"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_packages_payload_settings_default-destination_applications.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_install_location="/Applications"

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory,'package.pkg','PackageInfo'))

root = tree.getroot()

install_location = root.attrib['install-location']

if (expected_install_location == install_location):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
    print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
    print("    Expected: '{}' ; Found: \033[91m'{}'\033[0m".format(expected_install_location,install_location))



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
