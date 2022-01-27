#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

# Check that the build path for the package defined as the BUILD_PATH user defined setting uses the default value

test_displayed_name="uds > raw package > build path - default value"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_rawpackage_build_path.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_build_path='default'

expectedfilepath=os.path.join(dirname, '{}'.format(expected_build_path), 'raw_package.pkg')

if os.path.isfile(expectedfilepath):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
	
# Cleanup

shutil.rmtree(os.path.join(dirname, '{}'.format(expected_build_path)))

sys.exit()
