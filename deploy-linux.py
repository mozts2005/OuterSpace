#!/usr/bin/env python
from optparse import OptionParser
import os
import re
import shutil
import sys

parser = OptionParser()
parser.add_option("-f", "--force", dest = "force", action = "store_true",
    default = False, help = "Bypass SVN checks")
parser.add_option("-v", "--version", dest = "version", action = "store",
    default = "0.0.0a", help = "Set version (format N.N.NS)")
parser.add_option("", "--nosrc", dest = "source", action = "store_false",
    default = True, help = "Disable build of source distribution")
options, args = parser.parse_args()

## break version info into tuple
match = re.match("(\d+)\.(\d+)\.(\d+)(\w*)", options.version)
if match:
    version = match.group(1), match.group(2), match.group(3), match.group(4)
else:
    print "Cannot parse version string N.N.NS format required"

# retrieve revision
fd = os.popen("svn info .")
for line in fd:
    if line.startswith("Revision"):
        revision = int(line[len("Revision: "):])
fd.close()

# generate version file
fh = open("client-pygame/lib/osci/versiondata.py", "w")
print >> fh, """\
#
# This is generated file, please, do not edit
#
revision = %d
version = %s, %s, %s, "%s"
""" % (
    revision,
    version[0], version[1], version[2], version[3],
)
fh.close()

# check for modified files
if not options.force:
    print "#\n# Checking for modified and unversioned files"
    lines = os.popen("svn status").readlines()
    if lines:
        print "".join(lines)
        print "Fix problems displayed above and re-deploy"
        sys.exit(1)
    
# make client
os.chdir('client-pygame')
if options.source:
    os.system('python setup.py sdist')

os.system('python client-setup.py --name=ospace1 --longname="Outer Space" --version=%s --module=main.py ../server/website/client' % options.version)
os.chdir('..')

# copy version
shutil.copy2('client-pygame/lib/osci/version.py', 'server/lib/ige/ospace/ClientVersion.py')
shutil.copy2('client-pygame/lib/osci/versiondata.py', 'server/lib/ige/ospace/versiondata.py')

