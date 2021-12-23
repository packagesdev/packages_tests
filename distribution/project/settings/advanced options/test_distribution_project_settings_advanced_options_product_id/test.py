#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the product id is correctly set during the build process

test_displayed_name="distribution > project > settings > advanced option > product id"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_project_settings_advanced_options_product_id.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_product_id='com.mygreatcompany.application'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory, 'Distribution'))

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
