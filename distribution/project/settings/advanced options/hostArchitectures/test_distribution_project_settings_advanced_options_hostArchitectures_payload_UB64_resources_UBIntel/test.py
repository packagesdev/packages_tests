#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..','..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the hostArchitectures value is automatically set to x86_64 when the payload contains a Universal 64-bit binary and the resources contain a Universal Intel binary

test_displayed_name="distribution > project > settings > advanced option > host architectures > payload: UB64 / resources: UBIntel"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_project_settings_advanced_options_hostArchitectures_payload_UB64_resources_UBIntel.pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_distribution_host_architectures='x86_64'


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
    print("    Expected: '{}' ; Found: \033[91m'{}'\033[0m".format(expected_distribution_host_architectures,host_architectures))

# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
