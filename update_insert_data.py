# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:46:31 2016

@author: Jungmin
"""
import codecs
import json
import os
import re
import xml.etree.ElementTree as ET

from pymongo import MongoClient

filename = "boston_massachusetts.osm" # osm filename
path = "C:\Users\Jungmin\Downloads" # directory contain the osm file
OSMFILE = os.path.join(path, filename)
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# UPDATE THIS VARIABLE
mapping = { "Ave": "Avenue",
            "Ave.": "Avenue",
            "Ct": "Court",
            "Cambrdige": "Cambrdige Center",      
            "Elm": "Elm Street", 
            "Fenway": "Fenway Yawkey Way",           
            "Hwy": "Highway",
            "HIghway": "Highway",
            "LOMASNEY WAY, ROOF LEVEL": "Lomasney Way",
            "Pkwy": "Parkway",
            "Pl": "Place", 
            "Rd": "Road",
            "ST": "Street",
            "Sq.": "Square",           
            "St": "Street",           
            "St,": "Street",
            "St.": "Street",
            "Street.": "Street",
            "rd.": "Road",           
            "st": "Street",
            "street": "Street",
            "First Street, Suite 1100": "First Street",
            "Franklin Street, Suite 1702": "Franklin Street",           
            "Kendall Square - 3": "Kendall Square",
            "First Street, Suite 303": "First Street",
            "South Station, near Track 6": "South Station, Summer Street",
            "PO Box 846028": "846028 Surface Road",
            "Holland": "Holland Albany Street",
            "Windsor": "Windsor Stearns Hill Road",
            "Winsor": "Winsor Village Pilgrim Road",
            "Newbury": "Newbury Street",
            "First Street, 18th floor": "First Street",
            "Sidney Street, 2nd floor": "Sidney Street",           
            "Federal": "Federal Street",
            "Boylston Street, 5th Floor": "Boylston Street",
            "Hampshire": "Hampshire Street",
            "Webster Street, Coolidge Corner": "Webster Street",
            "Furnace Brook": "Furnace Brook Parkway",           
            "Faneuil Hall": "Faneuil Hall Market Street",
           }

mapping_zip = { "0239": "00000",
                "01238": "00000",
                "02132-3226": "02132",
                "02138-2742": "02138",
                "02134-1327": "02134",
                "02131-4931": "02131",
                "02445-5841": "02445",
                "02134-1322": "02134",
                "02134-1321": "02134",
                "02134-1305": "02134",
                "02138-1901": "02138",
                "02134-1306": "02134",
                "02138-2933": "02138",
                "02140-2215": "02140",
                "02474-8735": "02474",
                "01240": "00000",
                "02130-4803": "02130",
                "02114-3203": "02114",
                "02134-1316": "02134",
                "02134-1318": "02134",
                "MA 02118": "02118",
                "MA 02116": "02118",
                "01944": "00000",
                "01125": "00000",
                "02138-2736": "02138",
                "02134-1433": "02134",
                "Mass Ave": "00000",
                "02110-1301": "02110",
                "MA 02186": "02186",
                "02138-2903": "02138",
                "02134-1409": "02134",
                "02138-3003": "02138",
                "02138-2735": "02138",
                "02132-1239": "02132",
                "01250": "00000",
                "02134-1420": "02134",
                "02134-1307": "02134",
                "02138-2701": "02138",
                "02445-7638": "02445",
                "02134-1319": "02134",
                "02138-2762": "02138",
                "02138-2763": "02138",
                "02138-2706": "02138",
                "02026-5036": "02026",
                "02138-2724": "02138",
               }

def update_name(name, mapping):
    for key in mapping.keys():
        if name.find(key) != -1:
            name = name[:name.find(key)]+mapping[key]

    return name
    


def update_zipcode(zipcode, mapping_zip):
    for key in mapping_zip.keys():
        if zipcode.find(key) != -1:
            zipcode = zipcode[:zipcode.find(key)]+mapping_zip[key]
    return zipcode    


def shape_element(element):
    node = {}
    node["created"]={}
    node["address"]={}
    node["pos"]=[]
    refs=[]

    if element.tag == "node" or element.tag == "way" :
        if "id" in element.attrib:
            node["id"]=element.attrib["id"]
        node["type"]=element.tag

        if "visible" in element.attrib.keys():
            node["visible"]=element.attrib["visible"]

        for elem in CREATED:
            if elem in element.attrib:
                node["created"][elem]=element.attrib[elem]
        if "lat" in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))

        for tag in element.iter("tag"):
            if not(problemchars.search(tag.attrib['k'])):
                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"]=tag.attrib['v']
                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"]=tag.attrib['v']
                    node["address"]["postcode"] = update_zipcode(node["address"]["postcode"], mapping_zip)                      
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"]=tag.attrib['v']
                    node["address"]["street"] = update_name(node["address"]["street"], mapping)                 
                if tag.attrib['k'].find("addr")==-1:
                    node[tag.attrib['k']]=tag.attrib['v']
        for nd in element.iter("nd"):
             refs.append(nd.attrib["ref"])
        if node["address"] =={}:
            node.pop("address", None)
        if refs != []:
           node["node_refs"]=refs
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

# process the file
data = process_map(OSMFILE, True)   
 
client = MongoClient()
db = client.Boston
collection = db.bostonMAP
collection.insert(data)
collection


# size of the original xml file
os.path.getsize(OSMFILE)/1024/1024

# size of the processed json file
os.path.getsize(os.path.join(path, "boston_massachusetts.osm.json"))/1024/1024

# Number of unique users
len(collection.group(["created.uid"], {}, {"count":0}, "function(o, p){p.count++}"))

# Number of nodes
collection.find({"type":"node"}).count()

# Number of ways
collection.find({"type":"way"}).count()

# Top three users with most contributions

pipeline = [{"$group":{"_id": "$created.user",
                       "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 3}]
result = collection.aggregate(pipeline)

for x in xrange(3):
    get_record = result.next()
    print get_record
    
# Proportion of the top three users' contributions
pipeline = [{"$group":{"_id": "$created.user",
                       "count": {"$sum": 1}}},
            {"$project": {"proportion": {"$divide" :["$count",collection.find().count()]}}},
            {"$sort": {"proportion": -1}},
            {"$limit": 3}]

result = collection.aggregate(pipeline)

for x in xrange(3):
    get_record = result.next()
    print get_record    