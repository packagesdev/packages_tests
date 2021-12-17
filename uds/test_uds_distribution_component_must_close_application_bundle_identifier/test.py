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

# Check that the bundle identifier of the application that must be closed defined as the APPLICATION_BUNDLE_IDENTIFIER user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > component > must close application bundle identifier - dynamic value"

# Given

user_defined_application_bundle_identifier='inc.acme.test'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_component_must_close_application_bundle_identifier.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath, 'APPLICATION_BUNDLE_IDENTIFIER={}'.format(user_defined_application_bundle_identifier)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_application_bundle_identifier='inc.acme.test'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory, 'Distribution'))




root = tree.getroot()
pkgref_nodes = root.findall("pkg-ref")

found = False

for node in pkgref_nodes:

	if ( node.attrib['id'] == "com.mygreatcompany.pkg.package" ):
	
		mustClose_nodes_nodes=node.findall("must-close")
		
		for mustClose_node in mustClose_nodes_nodes:
		
			applications_nodes=mustClose_node.findall("app")
			
			for application_node in applications_nodes:
			
				if (application_node.attrib['id'] == expected_application_bundle_identifier):
					
					found=True
					
					break

if (found == True):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
