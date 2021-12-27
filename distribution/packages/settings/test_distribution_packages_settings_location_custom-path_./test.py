#!/usr/bin/env python2

import os
import errno
import sys
import subprocess
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'xar'))
import xar

import xml.etree.ElementTree as ET

# Check that the package is created at the same level as the distribution

test_displayed_name="distribution > packages > settings > location > custom path - ./"

# Given

dirname = os.path.dirname(__file__)
projectpath = os.path.join(dirname, 'test_distribution_packages_settings_location_custom-path_..pkgproj')

# When

process = subprocess.Popen(['/usr/local/bin/packagesbuild', '--project', projectpath ],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()


# Then

expected_reference_path="file:././package.pkg"

build_directory=os.path.join(dirname, 'build')

extraction_directory=os.path.join(dirname, 'extracted')

xar.expandPackageToDirectory(os.path.join(build_directory, 'distribution.pkg'),extraction_directory)

if (os.path.exists(os.path.join(build_directory, 'package.pkg')) == False ):
    
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

    if (package_file_reference_text == expected_reference_path):
        print("[+] " + test_displayed_name + ": " + '\033[1m' + "Success" + '\033[0m')
    else:
        print("[-] " + test_displayed_name + ": " + '\033[91m' + "Failure" + '\033[0m')



# Cleanup

shutil.rmtree(build_directory)
shutil.rmtree(extraction_directory)

sys.exit()
