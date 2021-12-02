#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

import xml.etree.ElementTree as ET

# Check that the path of the elastic folder defined by the ELASTIC_FOLDER_NAME user defined setting is correctly converted during the build process

test_displayed_name="uds > raw package > payload - elastic folder - dynamic value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_elastic_folder.pkgproj')

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

expected_elastic_folder_relative_path='default'

process = subprocess.Popen(['/usr/bin/lsbom', '-ds', 'Bom'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

all_directories_paths = list(stdout.split('\n'))

if (all_directories_paths[2] == "./Applications/{}".format(expected_elastic_folder_relative_path)):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

# Cleanup

os.chdir('..')

shutil.rmtree('build')
shutil.rmtree('extracted')

sys.exit()


