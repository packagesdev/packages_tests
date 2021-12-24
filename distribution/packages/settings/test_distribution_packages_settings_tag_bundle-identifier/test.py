#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the identifier is set to the value defined in the settings during the build process

test_displayed_name="distribution > packages > settings > tag > identifier"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_packages_settings_tag_bundle-dentifier.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_identifier="com.mygreatcompany.pkg.package"

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory,'package.pkg','PackageInfo'))

root = tree.getroot()

identifier = root.attrib['identifier']

if (expected_identifier == identifier):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
    print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
    print("    Expected: '{}' ; Found: \033[91m'{}'\033[0m".format(expected_identifier,identifier))



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
