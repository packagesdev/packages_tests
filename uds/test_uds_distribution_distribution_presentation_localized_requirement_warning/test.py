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

# Check that the warning components of the distribution requirement defined as the LOCALIZED_WARNING_TITLE and LOCALIZED_WARNING_MESSAGE user defined settings are correctly converted during the build process

test_displayed_name="uds > distribution > requirement > localized warning - dynamic value"

# Given

user_defined_requirement_warning_title='English Title'
user_defined_requirement_warning_message='English Message'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_presentation_localized_requirement_warning.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'LOCALIZED_WARNING_TITLE={}'.format(user_defined_requirement_warning_title) , 'LOCALIZED_WARNING_MESSAGE={}'.format(user_defined_requirement_warning_message)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_localizable_string_line_1=u'\"REQUIREMENT_FAILED_MESSAGE_INSTALLATION_CHECK_1\" = \"English Title\";'
expected_localizable_string_line_2=u'\"REQUIREMENT_FAILED_DESCRIPTION_INSTALLATION_CHECK_1\" = \"English Message\";'

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


found_1 = False
found_2 = False

for line in codecs.open(os.path.join(dirname, 'extracted', 'Resources', 'en.lproj', 'Localizable.strings'), encoding='utf-16'):
	
	if u'REQUIREMENT_FAILED_MESSAGE_INSTALLATION_CHECK_1' in line:
		
		line = line.rstrip('\r\n')
		
		if (line == expected_localizable_string_line_1):
			found_1 = True
			
	if u'REQUIREMENT_FAILED_DESCRIPTION_INSTALLATION_CHECK_1' in line:
		
		line = line.rstrip('\r\n')
		
		if (line == expected_localizable_string_line_2):
			found_2 = True


if (found_1 == True and found_2 == True):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
