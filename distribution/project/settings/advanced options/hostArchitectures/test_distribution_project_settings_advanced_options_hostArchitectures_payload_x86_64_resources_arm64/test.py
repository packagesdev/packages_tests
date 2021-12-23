#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..','..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the hostArchitectures value is automatically not set when the payload contains a x86_64 binary and the resources contain a arm64 binary

test_displayed_name="distribution > project > settings > advanced option > host architectures > payload: x86_64 / resources: arm64"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_project_settings_advanced_options_hostArchitectures_payload_x86_64_resources_arm64.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_host_architectures='arm64'


build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)


tree=ET.parse(os.path.join(extraction_directory, 'Distribution'))

root = tree.getroot()
options_node = root.find("options")

if not 'hostArchitectures' in options_node.attrib:
    print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
else:
    print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')
    print("    Expected: no hostArchitectures ; Found: \033[91m'{}'\033[0m".format(options_node.attrib['hostArchitectures']))

# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
