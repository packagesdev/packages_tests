#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

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

# Check that the name of the file defined by the DESTINATION_NAME user defined setting is correctly converted during the build process

test_displayed_name="uds > raw package > payload > destination name - dynamic value"

# Given

user_defined_custom_destination_name='.destination'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_payload_destination_name.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath , 'DESTINATION_NAME={}'.format(user_defined_custom_destination_name)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_file_name='.destination'

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'raw_package.pkg'),extraction_directory)

	# Check lsbom output

process = subprocess.Popen(['/usr/bin/lsbom', '-fs', os.path.join(dirname, 'extracted','Bom')],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

all_directories_paths = list(stdout.split('\n'))

if (all_directories_paths[0] == "./Applications/{}".format(expected_file_name)):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()


