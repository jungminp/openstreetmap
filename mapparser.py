# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:13:59 2016

@author: Jungmin
"""

import os
import pprint
import xml.etree.ElementTree as ET


filename = "boston_massachusetts.osm" # osm filename
path = "C:\Users\Jungmin\Downloads" # directory contain the osm file
OSMFILE = os.path.join(path, filename)

# iterative parsing
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag not in tags:
            tags[elem.tag] = 1
        else:
            tags[elem.tag] += 1
    return tags


tags = count_tags(OSMFILE)
pprint.pprint(tags)