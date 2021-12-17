#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil
import codecs

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the warning components of the distribution requirement defined as the EXTERNAL_SCRIPT_ARGUMENT user defined settings are correctly converted during the build process

test_displayed_name="uds > distribution > requirement > external script argument - dynamic value"

# Given

user_defined_requirement_external_script_argument='argument'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_requirement_external_script_argument.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'EXTERNAL_SCRIPT_ARGUMENT={}'.format(user_defined_requirement_external_script_argument) ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_source_line="		var tScriptArguments0=new Array('argument');"

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory, 'Distribution'))

root = tree.getroot()
script_node = root.find("script")

script_source=script_node.text

found=False

for line in script_source.splitlines():

	if (line == expected_source_line):
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
