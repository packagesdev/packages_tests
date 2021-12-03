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

	os.chdir(inDirectory)
	
	process = subprocess.Popen(['/usr/bin/xar', '-x', '-f' , inPackage],
						 stdout=subprocess.PIPE, 
						 stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()

# Check that the name of the distribution defined as the PRODUCT_VERSION user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > advanced option > product version - dynamic value"

# Given

user_defined_product_id='1.2.3'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_advanced_options_product_version.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath , 'PRODUCT_VERSION={}'.format(user_defined_product_id)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_product_version='1.2.3'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


os.chdir(extraction_directory)


tree=ET.parse('Distribution')

root = tree.getroot()
options_node = root.find("product")

product_version=options_node.attrib['version']

if (product_version == expected_distribution_product_version):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
