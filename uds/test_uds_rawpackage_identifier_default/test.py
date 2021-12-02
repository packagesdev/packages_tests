#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

import xml.etree.ElementTree as ET

# Check that the identifier of the package set by the PACKAGE_IDENTIFIER user defined setting uses the default value

test_displayed_name="uds > raw package > identifier - default"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_identifier.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_identifier='default'

relative_filepath=os.path.join('..', 'build', 'raw_package.pkg')

extract_folder=os.path.join(dirname, 'extracted')

os.mkdir(extract_folder)

os.chdir(extract_folder)
	

process = subprocess.Popen(['/usr/bin/xar', '-x', '-f' , relative_filepath],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()



tree=ET.parse('PackageInfo')

root = tree.getroot()

version = root.attrib['identifier']

if (version == expected_identifier):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

# Cleanup

os.chdir('..')

shutil.rmtree('build')
shutil.rmtree('extracted')

sys.exit()


