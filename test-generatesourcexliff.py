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

#generates an xliff source file for transifex from xbmc xml file
#usage: first parameter: xml file

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
for s in minidom.parse(sys.argv[1]).getElementsByTagName('string'):
  ids[s.attributes['id'].value]=getText(s.childNodes)

#the lame way to generate xml
print """<xliff>
 <file>
  <body>"""
for id in sorted(ids.keys(),key=int):
    print """
   <trans-unit id="%s">
    <context-group><context context-type="id">%s</context><context context-type="context">Sample Context</context></context-group>
    <source>%s</source>
   </trans-unit>"""%(id.encode("utf-8"), id.encode("utf-8"), ids[id].encode("utf-8").replace("&","&amp;").replace('"','&quot;'))

print """
  </body>
 </file>
</xliff>
"""
