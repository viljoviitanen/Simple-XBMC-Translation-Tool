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
ids=dict()

for d in doms:
  for s in d.getElementsByTagName('string'):
    ids[s.attributes['id'].value]=''

#loop all mentioned string ids, see if all the files have them
#not very efficient but I DONT CARE. Fix it if you care enough about this
for id in ids.keys():
  for i in range(len(myargs)):
    myids=[]
    for s in doms[i].getElementsByTagName('string'):
      myids.append(s.attributes['id'].value)
    if id not in myids:
      print "id %s missing in %s"%(id,myargs[i])


