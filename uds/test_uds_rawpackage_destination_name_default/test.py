#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

import xml.etree.ElementTree as ET

# Check that the name of the file defined by the DESTINATION_NAME user defined setting uses the default value set

test_displayed_name="uds > raw package > payload - destination name - default"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_destination_name.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

relative_filepath=os.path.join('..', 'build', 'raw_package.pkg')

extract_folder=os.path.join(dirname, 'extracted')

os.mkdir(extract_folder)

os.chdir(extract_folder)
	

process = subprocess.Popen(['/usr/bin/xar', '-x', '-f' , relative_filepath],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


	# Check lsbom output

expected_file_name='default'

process = subprocess.Popen(['/usr/bin/lsbom', '-fs', 'Bom'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

all_directories_paths = list(stdout.split('\n'))

if (all_directories_paths[0] == "./Applications/{}".format(expected_file_name)):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

# Cleanup

os.chdir('..')

shutil.rmtree('build')
shutil.rmtree('extracted')

sys.exit()


