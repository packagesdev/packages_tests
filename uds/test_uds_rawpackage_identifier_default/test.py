#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'xar'))
import xar

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

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'raw_package.pkg'),extraction_directory)

tree=ET.parse(os.path.join(extraction_directory,'PackageInfo'))

root = tree.getroot()

version = root.attrib['identifier']

if (version == expected_identifier):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()


