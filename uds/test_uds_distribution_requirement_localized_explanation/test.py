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

# Check that the explanation of the distribution requirement defined as the LOCALIZED_EXPLANATION user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > requirement > localized explanation - dynamic value"

# Given

user_defined_requirement_explanation='English Explanation'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_requirement_localized_explanation.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'LOCALIZED_EXPLANATION={}'.format(user_defined_requirement_explanation)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_localizable_string_line=u'\"REQUIREMENT_FAILED_MESSAGE_VOLUME_CHECK_1\" = \"English Explanation\";'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


found = False

for line in codecs.open(os.path.join(dirname, 'extracted', 'Resources', 'en.lproj', 'Localizable.strings'), encoding='utf-16'):
	
	if u'REQUIREMENT_FAILED_MESSAGE_VOLUME_CHECK_1' in line:
		
		line = line.rstrip('\r\n')
		
		if (line == expected_localizable_string_line):
			found = True


if (found == True):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
