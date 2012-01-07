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

import sys

myargs=sys.argv

#get only the the command line agruments
myargs[0:1]=[]

doms=[]
for i in range(len(myargs)):
  print "Parsing: " + myargs[i]
  doms.append(minidom.parse(myargs[i]))

#get all ids from all files
allids=dict()
ids=[]

#store all ids in one dictionary and ids per file in separate dictionaries
for i in range(len(myargs)):
  ids.append(dict());
  for s in doms[i].getElementsByTagName('string'):
    allids[s.attributes['id'].value]=''
    ids[i][s.attributes['id'].value]=''

#loop all mentioned string ids, see if all the files have them
for id in allids.keys():
  for i in range(len(myargs)):
    if id not in ids[i].keys():
      print "id %s missing in %s"%(id,myargs[i])


