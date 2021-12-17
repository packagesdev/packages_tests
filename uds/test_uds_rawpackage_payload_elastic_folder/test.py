#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the path of the elastic folder defined by the ELASTIC_FOLDER_NAME user defined setting is correctly converted during the build process

test_displayed_name="uds > raw package > payload > elastic folder - dynamic value"

# Given

user_defined_elastic_folder_name='my/custom/folder'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_payload_elastic_folder.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath , 'ELASTIC_FOLDER_NAME={}'.format(user_defined_elastic_folder_name)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_elastic_folder_relative_path='my/custom/folder'

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'raw_package.pkg'),extraction_directory)


	# Check lsbom output

process = subprocess.Popen(['/usr/bin/lsbom', '-ds', os.path.join(dirname, 'extracted','Bom')],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

all_directories_paths = list(stdout.split('\n'))

if (all_directories_paths[4] == "./Applications/{}".format(expected_elastic_folder_relative_path)):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()


