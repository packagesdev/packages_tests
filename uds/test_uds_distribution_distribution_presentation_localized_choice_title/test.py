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


# Check that the title of the first choice defined as the CHOICE_TITLE user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > presentation > localized choice title - dynamic value"

# Given

user_defined_presentation_choice_title='English Choice Title'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_presentation_localized_choice_title.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'CHOICE_TITLE={}'.format(user_defined_presentation_choice_title)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_localizable_string_line=u'\"INSTALLER_CHOICE_1_TITLE\" = \"English Choice Title\";'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


found = False

for line in codecs.open(os.path.join(dirname, 'extracted', 'Resources', 'en.lproj', 'Localizable.strings'), encoding='utf-16'):
	if u'INSTALLER_CHOICE_1_TITLE' in line:
		
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
