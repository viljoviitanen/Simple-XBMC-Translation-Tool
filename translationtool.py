#!/usr/bin/python
#Copyright (C) 2012  Viljo Viitanen <viljo.viitanen@iki.fi> and contributors.
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import copy
import sys
from xml.dom import minidom


# From python reference manual
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def main(argv=None):
    if argv is None:
        argv = sys.argv

    file1 = argv[1]

    # First, parse the base file. store ids and text values in a dictionary for
    # fast access later
    print "Using base: " + file1
    allids = dict()
    baseids = dict()
    for s in minidom.parse(file1).getElementsByTagName('string'):
        baseids[s.attributes['id'].value] = getText(s.childNodes)
        allids[s.attributes['id'].value] = ''
        #print "base: %s %s"%(s.attributes['id'].value.encode("utf-8"),getText(s.childNodes).encode("utf-8"))

    # Get only the the command line arguments 2-n
    myargs = copy.deepcopy(argv[2:])

    doms = []
    for arg in myargs:
        #print "Parsing: " + arg
        doms.append(minidom.parse(arg))

    # Get all ids from all files
    ids = []
    # Store all ids in one dictionary and ids per file in separate dictionaries
    for i in range(len(myargs)):
        ids.append(dict())
        for s in doms[i].getElementsByTagName('string'):
            allids[s.attributes['id'].value] = ''
            ids[i][s.attributes['id'].value] = ''

    # Loop all files, see if all ids are found
    for i, arg in enumerate(myargs):
        print arg
        for id in sorted(allids.keys()):
            if id not in ids[i].keys():
                if id in baseids.keys():
                    print """  <string id="%s">%s</string>""" % (id.encode("utf-8"), baseids[id].encode("utf-8"))
            elif id in ids[i].keys() and id not in baseids.keys():
                print """  not in base:%s"""%(id.encode("utf-8"))

if __name__ == '__main__':
    sys.exit(main())
