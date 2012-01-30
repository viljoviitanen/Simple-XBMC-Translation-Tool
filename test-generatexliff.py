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
#print "Using base: "+sys.argv[1]
allids=dict()
baseids=dict()
for s in minidom.parse(sys.argv[1]).getElementsByTagName('string'):
  baseids[s.attributes['id'].value]=getText(s.childNodes)
  allids[s.attributes['id'].value]=''
  #print "base: %s %s"%(s.attributes['id'].value.encode("utf-8"),getText(s.childNodes).encode("utf-8"))

#get only the the command line agruments 2-n
myargs=copy.deepcopy(sys.argv)
myargs[0:2]=[]

doms=[]
for i in range(len(myargs)):
  #print "Parsing: " + myargs[i]
  doms.append(minidom.parse(myargs[i]))

#get all ids from all files
ids=[]
#store all ids in one dictionary and ids per file in separate dictionaries
for i in range(len(myargs)):
  ids.append(dict());
  for s in doms[i].getElementsByTagName('string'):
    allids[s.attributes['id'].value]=''
    ids[i][s.attributes['id'].value]=getText(s.childNodes)

print """<xliff>
  <file>
    <body>"""
#loop all files, see if all ids are found
for i in range(len(myargs)):
#  print myargs[i]
  for id in sorted(allids.keys()):
    try:
      translation=ids[i][id].encode("utf-8").replace("&","&amp;").replace('"','&quot;')
    except KeyError:
      translation="[ XXXXX MISSING ]"
    print """
      <trans-unit id="%s">
        <context-group><context context-type="x-id">%s</context></context-group>
        <source>%s</source>
        <target>%s</target> 
      </trans-unit>"""%(id.encode("utf-8"), id.encode("utf-8") ,baseids[id].encode("utf-8").replace("&","&amp;").replace('"','&quot;')
                        ,translation)

print """
    </body>
  </file>
</xliff>
"""
