# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:36:16 2016

@author: Jungmin
"""
import os
import pprint
import xml.etree.ElementTree as ET

filename = "boston_massachusetts.osm" # osm filename
path = "C:\Users\Jungmin\Downloads" # directory contain the osm file
OSMFILE = os.path.join(path, filename)

def unique_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib.keys():
            if element.attrib['uid'] not in users:
                users.add(element.attrib['uid'])

    return users


users = unique_users(OSMFILE)
pprint.pprint(users)