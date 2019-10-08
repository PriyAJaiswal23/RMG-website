#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script automatically updates the header for *.py, *.pyx, and *.pxd
files in RMG-Py/rmgpy, RMG-Py/scripts, and the root RMG-Py directory.

Other directories (e.g., examples, documentation, etc.) are ignored
along with directories containing test data.

The headers are automatically generated based on the LICENSE.txt file.
Typical usage would involve running this script after updating the copyright
date in the license file.

Because this script makes assumptions regarding the contents at the
start of each file, be sure to double-check the results to make sure
important lines aren't accidentally overwritten.
"""
from __future__ import print_function

import os

shebang = "#!/usr/bin/env python3"

header = """###############################################################################
#                                                                             #
# RMG Website - A Django-powered website for Reaction Mechanism Generator     #
#                                                                             #
"""

with open('LICENSE.txt', 'r') as f:
    for line in f:
        line = line.strip()
        newline = '# {0:<75} #\n'.format(line)
        header += newline

header += """#                                                                             #
###############################################################################
"""

print(header)


def replace_header(oldfile):
    newfile = os.path.join('tmp', 'tempfile')

    ext = os.path.splitext(oldfile)[1]
    if ext != '.py':
        raise Exception('Unexpected file type: {0}'.format(oldfile))

    with open(oldfile, 'r') as old, open(newfile, 'w+') as new:

        # Write shebang and encoding
        new.write(shebang)

        # Read old file and copy over contents
        found_bar = False
        first_line = True
        start = False
        for i, line in enumerate(old):
            if i == 0 and line[0] != '#':
                # Assume there's no header, so start copying lines right away
                new.write(header)
                start = True
            if start:
                if first_line and line.strip() != '':
                    new.write('\n')
                first_line = False
                new.write(line)
            elif line.startswith('##########'):
                if found_bar:
                    # We've reached the end of the license, so start copying lines starting with the next line
                    new.write(header)
                    start = True
                else:
                    found_bar = True

    # Replace old file with new file
    os.rename(newfile, oldfile)


# Create temporary directory for writing files
if not os.path.exists('tmp'):
    os.makedirs('tmp')

# Compile list of files to modify
filelist = ['manage.py']

root_dirs = ['rmgweb']
for root_dir in root_dirs:
    for root, dirs, files in os.walk(root_dir):
        print(root)
        for f in files:
            ext = os.path.splitext(f)[1]
            if ext in ['.py']:
                filelist.append(os.path.join(root, f))

for f in filelist:
    print('Updating {0} ...'.format(f))
    replace_header(f)
