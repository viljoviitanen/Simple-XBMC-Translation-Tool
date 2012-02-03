#!/usr/bin/python
#Copyright (C) 2012  Viljo Viitanen <viljo.viitanen@iki.fi>
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

#generates an xbmc xml file from transifex xliff 
#usage: first parameter: xliff file

from xml.dom import minidom

import sys,copy

#from python reference manual
def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

#first, parse the base file. store ids and text values in a dictionary for fast access later
ids=dict()
for t in minidom.parse(sys.argv[1]).getElementsByTagName('trans-unit'):
  try:
    ids[t.attributes['id'].value]=getText(t.getElementsByTagName('target')[0].childNodes)
  except IndexError:
    #if no target elements where found, just skip
    pass

#the lame way to generate xml
print """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<strings>"""
for id in sorted(ids.keys(),key=int):
    print """  <string id="%s">%s</string>"""%(id.encode("utf-8"), ids[id].encode("utf-8").replace("&","&amp;")
                                               . replace("\n",'&#10;'))

print """
</strings>
"""
