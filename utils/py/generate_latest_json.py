#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_update_info.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" This script generates an latest.json file used by Cnchi to check the latest version """

import os
import hashlib
import sys

CNCHI_PATH = "/usr/share/cnchi"
sys.path.append(CNCHI_PATH)
sys.path.append(os.path.join(CNCHI_PATH, "cnchi"))

import cnchi.info as info


def get_md5(file_name):
    """ Gets md5 hash from a file """
    md5_hash = hashlib.md5()
    with open(file_name, "rb") as myfile:
        for line in myfile:
            md5_hash.update(line)
    return md5_hash.hexdigest()


def get_files(path):
    """ Returns all files from a directory """
    all_files = []
    skip_names = ["__pycache__", ".git", "CHANGES", "info.py", "latest.json", ".tx/", "utils/"]
    if os.path.exists(path):
        for dpath, d, files in os.walk(path):
            for f in files:
                file_path = os.path.join(dpath, f)
                path_OK = True
                for skip in skip_names:
                    if skip in file_path:
                        path_OK = False
                if path_OK:
                    all_files.append(file_path)
    else:
        all_files = False

    return all_files


def create_update_info():
    """ Creates update.info file """

    myfiles = get_files("/usr/share/cnchi") or get_files(".")

    txt = '{{"version":"{}"}}'.format(info.CNCHI_VERSION)

    # for filename in myfiles:
    #     md5 = get_md5(filename)
    #     if "usr/share/cnchi" not in filename:
    #         filename = filename.replace('./', '/usr/share/cnchi/')
    #     txt += '{"name":"%s","md5":"%s"},\n' % (filename, md5)

    # remove last comma and close
    # txt = txt[:-3]

    with open("dist/latest.json", "w") as update_info:
        update_info.write(txt)

if __name__ == '__main__':
    create_update_info()
