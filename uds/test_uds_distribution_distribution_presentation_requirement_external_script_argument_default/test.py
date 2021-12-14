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

# Check that the warning components of the distribution requirement defined as the EXTERNAL_SCRIPT_ARGUMENT user defined setting uses the default value set during the build process

test_displayed_name="uds > distribution > requirement > external script argument - default value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_presentation_requirement_external_script_argument.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_source_line="		var tScriptArguments0=new Array('default');"

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


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
