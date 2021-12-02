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

# Check that the name of the distribution defined as the HOST_ARCHITECTURES user defined setting uses the default value set during the build process

test_displayed_name="uds > distribution > advanced option > host architectures - default value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_advanced_options_hostArchitectures.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_host_architectures='i386'

relative_filepath=os.path.join('..', 'build', 'distribution.pkg')

extract_folder=os.path.join(dirname, 'extracted')

expandPackageToDirectory(relative_filepath,extract_folder)


tree=ET.parse('Distribution')

root = tree.getroot()
options_node = root.find("options")

host_architectures=options_node.attrib['hostArchitectures']

if (host_architectures == expected_distribution_host_architectures):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

os.chdir('..')

shutil.rmtree('build')
shutil.rmtree('extracted')

sys.exit()
