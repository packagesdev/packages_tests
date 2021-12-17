#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the name of the distribution defined as the HOST_ARCHITECTURES user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > advanced option > host architectures - dynamic value"

# Given

user_defined_host_architectures='arm64 x86_64'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_advanced_options_hostArchitectures.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath , 'HOST_ARCHITECTURES={}'.format(user_defined_host_architectures)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_host_architectures='arm64 x86_64'

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory, 'Distribution'))

root = tree.getroot()
options_node = root.find("options")

host_architectures=options_node.attrib['hostArchitectures']

if (host_architectures == expected_distribution_host_architectures):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
