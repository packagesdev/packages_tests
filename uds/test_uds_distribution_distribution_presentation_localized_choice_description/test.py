#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil
import codecs


import xml.etree.ElementTree as ET

def expandPackageToDirectory(inPackage,inDirectory):
	try:
    		os.makedirs(inDirectory)
	except OSError as e:
    		if e.errno != errno.EEXIST:
        		raise
	
	process = subprocess.Popen(['/usr/bin/xar', '-x', '-f' , inPackage, '-C', inDirectory],
						 stdout=subprocess.PIPE, 
						 stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()

# Check that the description of the first choice defined as the CHOICE_DESCRIPTION user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > presentation > localized choice description - dynamic value"

# Given

user_defined_presentation_choice_description='English Choice Description'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_presentation_localized_choice_description.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'CHOICE_DESCRIPTION={}'.format(user_defined_presentation_choice_description)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_localizable_string_line=u'\"INSTALLER_CHOICE_1_DESCRIPTION\" = \"English Choice Description\";'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


found = False

for line in codecs.open(os.path.join(dirname, 'extracted', 'Resources', 'en.lproj', 'Localizable.strings'), encoding='utf-16'):
	if u'INSTALLER_CHOICE_1_DESCRIPTION' in line:
		
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
