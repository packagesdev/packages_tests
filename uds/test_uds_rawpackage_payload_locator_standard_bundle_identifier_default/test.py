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

# Check that the app locator bundle identifier defined as the LOCATOR_BUNDLE_IDENTIFIER user defined setting uses the default value set during the build process

test_displayed_name="uds > raw package > payload > locator > standard bundle identifier - default value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_payload_locator_standard_bundle_identifier.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_locator_bundle_identifier='default'

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'raw_package.pkg'),extraction_directory)


found = False

tree=ET.parse(os.path.join(extraction_directory, 'PackageInfo'))

root = tree.getroot()

locator_search_node = root.find('locator')

search_nodes = locator_search_node.findall('search')

for search_node in search_nodes:

	if search_node.attrib['id'] == 'search.1.fr.whitebox.EmptyCocoaApp':
		
		bundle_nodes = search_node.findall('bundle')
		
		for bundle_node in bundle_nodes:

			
			if bundle_node.attrib['path'] == '/EmptyCocoaApp.app':
			
				if bundle_node.attrib['CFBundleIdentifier'] == expected_locator_bundle_identifier:
				
					found = True
				
					break


if (found == True):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')


# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
