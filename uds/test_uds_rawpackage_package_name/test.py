#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

# Check that the name of the package defined as the PACKAGE_NAME user defined setting is correctly converted during the build process

test_displayed_name="uds > raw package > package name - dynamic value"

# Given

user_defined_package_name='dynamic'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_package_name.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath , 'PACKAGE_NAME={}'.format(user_defined_package_name)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_package_name='dynamic'

expectedfilepath=os.path.join(dirname, 'build', '{}.pkg'.format(expected_package_name))

if os.path.isfile(expectedfilepath):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
	
# Cleanup

shutil.rmtree(os.path.join(dirname, 'build'))

sys.exit()
