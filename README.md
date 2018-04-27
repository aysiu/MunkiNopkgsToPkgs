# MunkiNopkgsToPkgs
Converts Munki nopkg items to pkgs (designed for printer nopkgs but may work for others)

## Purpose
This script was created for a specific use case: to convert [printer nopkg Munki items](https://github.com/munki/munki/wiki/Managing-Printers-With-Munki#nopkg-method) into pkgs instead. I wrote this because I had many, many printer nopkg items with installcheck_scripts, and it was actually taking too long (about 30 seconds total) to run them every single Munki run. It wasn't that important to know for absolute certain whether a printer is installed or not (one advantage of a nopkg is that you can tell whether the printer is installed or not, regardless of whether it was installed with a package or via System Preferences or some other method).

## Script Limitations
The script operates on some assumptions that make perfect sense for this particular use case (for example, that there is an uninstall_script, which there doesn't always have to be for a nopkg or that version numbers will be actual numbers instead of a combination of words and numbers). There is not a comprehensive set of sanity checks for key's existences or an easy way to resolve errors interactively (the script just exits with an error message if, for example, it's looking for a particular executable or directory and doesn't find it).

## Requirements
* You need [Munki tools](https://github.com/munki/munki/releases/latest) installed on whatever machine is running this script, because it makes use of `munkiimport` and `makecatalogs`.
* There are many ways to build packages in macOS. This script relies on [Munki-Pkg](https://github.com/munki/munki-pkg) to do so.

## Fork away!
If you would like to adapt this to be more foolproof for multiple situations, feel free to fork and/or provide pull requests. My initial goal here is not to create an all-purpose nopkg-to-pkg conversion script but to just help myself in this particular situation. That said, if people found a use for this script and wanted to adapt it to other nopkg-conversion scenarios, it's open source. Go for it!
