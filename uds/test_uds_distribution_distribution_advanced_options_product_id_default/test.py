#!/usr/bin/env python2

import os
import errno
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

# Check that the name of the distribution defined as the PRODUCT_ID user defined setting uses the default value set during the build process

test_displayed_name="uds > distribution > advanced option > product id - default value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_advanced_options_product_id.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_product_id='default'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


os.chdir(extraction_directory)

tree=ET.parse('Distribution')

root = tree.getroot()
options_node = root.find("product")

product_id=options_node.attrib['id']

if (product_id == expected_distribution_product_id):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
