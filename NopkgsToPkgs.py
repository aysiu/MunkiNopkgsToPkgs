#!/usr/bin/python

import os
import plistlib
import subprocess
import sys
import time

##################################################################
### Parameters to definitely change before running this script ###
# Directory of pkgsinfo to convert. DO NOT just convert the entire pkgsinfo on the Munki repo server. Copy to a separate directory just the nopkgs for conversion.
nopkgs_directory='/PATH/TO/COPIED/PKGSINFO/IN/NEED/OF/CONVERSION'

# Org package identifier
org='com.yourcompanyname.'
##################################################################

##################################################################
### Parameters to double-check before running this script ###
# Path to munkipkg binary
munkipkg='/usr/local/bin/munkipkg'

# Directory to put munkipkgs (not your Munki repo but some other temp directory)
munkipkg_dir='/tmp'

# munkiimport binary
munkiimport='/usr/local/munki/munkiimport'

# makecatalogs binary
makecatalogs='/usr/local/munki/makecatalogs'
##################################################################

# Main
def main():

	# Loop through the pkgsinfo
	if os.path.isdir(nopkgs_directory):
		for root, dirs, files in os.walk(nopkgs_directory):
			for dir in dirs:
				# Skip directories starting with a period
				if dir.startswith("."):
					dirs.remove(dir)
			for file in files:
				# Skip files that start with a period
				if file.startswith("."):
					continue
				# Get the full path to the file
				fullfile = os.path.join(root, file)
				
				# Get the plist info into a variable
				nopkg_plist=plistlib.readPlist(fullfile)
				print "Processing %s" % nopkg_plist['name']

				# Create the munkipkg directory based on the name of the item
				if os.path.isdir(munkipkg_dir):
					# Get the full path of what we want to create
					munkipkg_subdir=os.path.join(munkipkg_dir, nopkg_plist['name'])
					if not os.path.isdir(munkipkg_subdir):
						print "Getting plist information"
						os.mkdir(munkipkg_subdir)
						# Get identifier for package
						identifier=org+nopkg_plist['name']
						# Get the name for the package
						name=nopkg_plist['name']+'.pkg'
						# Get the version for the package
						version=str(float(nopkg_plist['version'])+1)
						# Define basic dictionary of build-info.plist keys and values
						build_info={ "distribution_style": False, "identifier": identifier, "install_location": "/", "name": name, "ownership": "recommended", "postinstall_action": "none", "version": version }
						# Write the build-info plist
						build_info_location=os.path.join(munkipkg_subdir, 'build-info.plist')
						plistlib.writePlist(build_info, build_info_location)
						# Make a directory for the postinstall script
						scripts=os.path.join(munkipkg_subdir, 'scripts')
						os.mkdir(scripts)
						postinstall=os.path.join(scripts, 'postinstall')
						f=open(postinstall, "w+")
						f.write(nopkg_plist['postinstall_script'])
						f.close()
						# We also need an empty payload, so a receipt gets left, too
						emptypayload=os.path.join(munkipkg_subdir, 'payload/tmp')
						os.makedirs(emptypayload)
						if os.path.isfile(munkipkg):
							print "Building a pkg"
							# Build the package using munkipkg
							cmd = [ munkipkg, munkipkg_subdir ]
							proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
							# Get the uninstall_script from the original nopkg
							uninstall=os.path.join(munkipkg_subdir, 'uninstall')
							f=open(uninstall, "w+")
							f.write(nopkg_plist['uninstall_script'])
							f.close()
							# Check the munkiimport binary exists
							if os.path.isfile(munkiimport):
								print "Importing into Munki"
								# Path to .pkg to import
								newpkg=os.path.join(munkipkg_subdir, 'build', name)
								category='--category=' + nopkg_plist['category']
								developer='--developer=' + nopkg_plist['developer']
								preuninstall_script='--preuninstall_script=' + uninstall
								itemname='--name=' + nopkg_plist['name']
								pkgvers='--pkgvers=' + version
								displayname='--displayname=' + nopkg_plist['display_name']
								# Import with munkiimport but non-interactively
								cmd = [ munkiimport, newpkg, displayname, '--unattended_uninstall', '--nointeractive', '--unattended_install', category, developer, preuninstall_script, pkgvers, itemname ]
								proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
								# Wait a few seconds, so there aren't too many open subprocesses
								time.sleep(3)
							else:
								print "Error: %s is not a valid path to munkiimport" % munkiimport
								sys.exit(1)
						else:
							print "Error: %s is not a valid path to munkipkg" % munkipkg
							sys.exit(1)
					else:
						print "Warning: %s subdirectory already exists in %s. Skipping." % (nopkg_plist['name'], munkipkg_dir)
				else:
					print "Error: %s is not a directory." % munkipkg_dir
					sys.exit(1)
		# After looping through everything, run makecatalogs
		if os.path.isfile(makecatalogs):
			print "Running makecatalogs"
			cmd = [ makecatalogs ]
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			print "Error: %s is not a valid path to makecatalogs" % makecatalogs
			sys.exit(1)
	else:
		print "Error: %s is not a directory." % nopkgs_directory		
		sys.exit(1)

if __name__ == '__main__':
	main()
