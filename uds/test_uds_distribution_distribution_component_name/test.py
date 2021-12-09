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

# Check that the name of the package component of the distribution as the COMPONENT_NAME user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > component > name - dynamic value"

# Given

user_defined_component_name='package'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_component_name.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'COMPONENT_NAME={}'.format(user_defined_component_name)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_component_name='package'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


if (os.path.exists(os.path.join(extraction_directory,'{}.pkg'.format(expected_component_name))) == False ):

	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')

else:

	tree=ET.parse(os.path.join(extraction_directory, 'Distribution'))

	root = tree.getroot()
	pkgref_nodes = root.findall("pkg-ref")

	package_file_reference_text = 'not found'

	for node in pkgref_nodes:

		if ( node.attrib['id'] == "com.mygreatcompany.pkg.package" ):
	
			if (len(node.text) > 0):
		
				package_file_reference_text = node.text
			
				break
		

	if (package_file_reference_text == "#{}.pkg".format(expected_component_name)):
		print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
	else:
		print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
