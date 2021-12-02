#!/usr/bin/env python2

import os
import sys
import subprocess
import shutil

# Check that the name of the distribution defined as the DISTRIBUTION_NAME user defined setting is correctly converted during the build process

test_displayed_name="uds > distribution > distribution name - dynamic value"

# Given

user_defined_distribution_name='dynamic'

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_uds_distribution_distribution_name.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath , 'DISTRIBUTION_NAME={}'.format(user_defined_distribution_name)],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_name='dynamic'

expectedfilepath=os.path.join(dirname, 'build', '{}.pkg'.format(expected_distribution_name))

if os.path.isfile(expectedfilepath):
	print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
	print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
	
# Cleanup

shutil.rmtree(os.path.join(dirname, 'build'))

sys.exit()
