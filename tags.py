# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:16:43 2016

@author: Jungmin
"""

import re
import os
import pprint
import xml.etree.ElementTree as ET


filename = "boston_massachusetts.osm" # osm filename
path = "C:\Users\Jungmin\Downloads" # directory contain the osm file
OSMFILE = os.path.join(path, filename)

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        key = element.attrib['k']
        if re.search(lower, key) != None:
            keys['lower'] += 1
        elif re.search(lower_colon, key) != None:
            keys['lower_colon'] += 1
        elif re.search(problemchars, key) != None:
            keys['problemchars'] += 1
            print(element.attrib['k'])
        else:
            keys['other'] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

keys = process_map(OSMFILE)
pprint.pprint(keys)