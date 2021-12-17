#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil
import codecs

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the copyright year for the custom license template defined as the CUSTOM_LICENSE_YEAR user defined setting uses the default value set during the build process

test_displayed_name="uds > distribution > presentation > custom license template keyword - default value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_presentation_custom_license_template_keyword.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_presentation_custom_license_template_keyword='default'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


found = False

for line in codecs.open(os.path.join(dirname, 'extracted', 'Resources', 'en.lproj', 'license.rtf'), encoding='utf-8'):
	
	if '\expndtw0 {}\expnd0'.format(expected_presentation_custom_license_template_keyword) in line:
		found = True


if (found == True):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
