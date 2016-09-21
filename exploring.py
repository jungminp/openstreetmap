# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:18:17 2016

@author: Jungmin
"""
import os
import pprint
import xml.etree.ElementTree as ET
from collections import defaultdict

filename = "boston_massachusetts.osm" # osm filename
path = "C:\Users\Jungmin\Downloads" # directory contain the osm file
OSMFILE = os.path.join(path, filename)

TAG_KEYS = ['addr:street', 'addr:postcode']
item_limit = 100
    
def examine_tags(osmfile, item_limit):
    print "Examining tag keys: {}".format(TAG_KEYS)
    osm_file = open(osmfile, "r")

    # initialize data with default set data structure
    data = defaultdict(set)

    # iterate through elements
    for _, elem in ET.iterparse(osm_file, events=("start",)):
        # check if the element is a node or way
        if elem.tag == "node" or elem.tag == "way":
            # iterate through children matching `tag`
            for tag in elem.iter("tag"):
                # skip if does not contain key-value pair
                if 'k' not in tag.attrib or 'v' not in tag.attrib:
                    continue
                key = tag.get('k')
                val = tag.get('v')
                # add to set if in tag keys of interest and is below the item limit
                if key in TAG_KEYS and len(data[key]) < item_limit:
                    data[key].add(val)
    return data

tag_data = dict(examine_tags(OSMFILE, item_limit))
pprint.pprint(tag_data)