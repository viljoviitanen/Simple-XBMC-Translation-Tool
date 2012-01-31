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

#generates an xliff file for transifex import
#usage: first parameter: English/strings.xml second parameter: Otherlanguage/strings.xml

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
baseids=dict()
for s in minidom.parse(sys.argv[1]).getElementsByTagName('string'):
  baseids[s.attributes['id'].value]=getText(s.childNodes)

#then the other file
ids=dict();
for s in minidom.parse(sys.argv[2]).getElementsByTagName('string'):
  ids[s.attributes['id'].value]=getText(s.childNodes)

#the lame way to generate xml
print """<xliff>
 <file>
  <body>"""
for id in sorted(baseids.keys(),key=int):
  try:
    translation=ids[id].encode("utf-8").replace("&","&amp;").replace('"','&quot;')
  except KeyError:
    translation=""
  print """
   <trans-unit id="%s">
    <context-group><context context-type="id">%s</context><context context-type="context">Sample Context</context></context-group>
    <source>%s</source>
    <target>%s</target> 
   </trans-unit>"""%(id.encode("utf-8"), id.encode("utf-8"), baseids[id].encode("utf-8").replace("&","&amp;").replace('"','&quot;'), translation)

print """
  </body>
 </file>
</xliff>
"""
