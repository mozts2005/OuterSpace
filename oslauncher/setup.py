from distutils.core import setup

havePy2Exe = False
try:
    import py2exe
    havePy2Exe = True
except ImportError:
    pass

import glob
import shutil
import os
import stat

if havePy2Exe:
    # collect data files
    data_files = [
        (".", ("ChangeLog", "COPYING", "README"))
    ]
    # resources
    for root, dirs, files in os.walk('res'):
        try: 
            dirs.remove(".svn")
        except ValueError:
            pass
    if files:
        data_files.append((root, [os.path.join(root, file) for file in files]))

else:
    data_files = [
        ("/usr/share/pixmaps", ("fedora/outerspace-icon.png",)),
        ("/usr/share/applications", ("fedora/fedora-outerspace.desktop",)),
        ("/usr/share/outerspace", glob.glob("res/*.ico")),
        ("/usr/share/outerspace", glob.glob("res/*.png")), 
        ("/usr/share/outerspace/gray", glob.glob("res/gray/*")), 
    ]

# no package data
package_data = {}

# version
version = (0, 2, 2)

open("oslauncher/versiondata.py", "w").write("""
#
# This is generated file, please, do not edit
#
version = %d, %d, %d
""" % version)

# setup
setup(
    name = 'outerspace',
    version = '%d.%d.%d' % version,
    license = "GPL",
    description = 'Launcher for Outer Space client',
    long_description = "The Outer Space Launcher keeps Outer Space client synchronized with the server",
    author = "Ludek Smid",
    author_email = "qark@ospace.net",
    maintainer = 'Ludek Smid',
    maintainer_email = 'qark@ospace.net',
    url = 'http://www.ospace.net/',
    windows = [
        {
            "script": "outerspace",
            "icon_resources": [(1, "oslauncher/res/smallicon.ico"), (1, "oslauncher/res/bigicon.ico")]
        }
    ],
    data_files = data_files,
    packages = ["oslauncher", "oslauncher.urlgrabber", "oslauncher.pgu", "oslauncher.pgu.gui"],
    package_data = package_data,
    scripts = ["outerspace"],
)
