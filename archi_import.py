import xml.etree.ElementTree as ET
import re
import sys
import mariadb

try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="eits"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
# Get Cursor
cur = conn.cursor()

def get_all_children(children, element):
    for child in element:
        if(re.search("^archimate" ,str(child.get("{http://www.w3.org/2001/XMLSchema-instance}type")))):
            children.append(child)
        if(len(child) > 0):
            get_all_children(children, child)
    return children

def add_data(sid, type, name, ipv4, os, vpc, stage, eol, ext_ipv4, vendor, url):
#    print(sid,type,name,ipv4,os,vpc,stage,eol)
    try: 
        cur.execute("INSERT INTO archi_import (sid, type, name, ipv4, os, vpc, stage, eol, ext_ipv4, vendor, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (sid, type, name, ipv4, os, vpc, stage, eol, ext_ipv4, vendor, url)) 
    except mariadb.Error as e: 
        print(f"Error adding data to MariaDB: {e}")
    conn.commit() 


tree = ET.parse('eits_demo.archimate')
x = 0
root = tree.getroot()
children = []
children = get_all_children(children, root)
for child in children:
    type = str(child.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
    name = str(child.get("name"))
    formattedType = type.split(":")
    type = formattedType[1]
    id = str(child.get("id"))
    if(name == "None"):
        name = None
    if type == "RealizationRelationship" or type == "AssignmentRelationship" or type == "ServingRelationship" or type == "AssociationRelationship" or type == "Connection" or type == "DiagramObject": 
        continue

    property_value = [None, None, None, None, None, None, None, None]
    property_key = ["IPV4", "OS", "VPC", "Stage", "EOL", "Ext_IPv4", "Vendor", "URL"]
    for property in child:
        for i in range(len(property_key)):
            if(property.get("key") == property_key[i]):
                property_value[i] = (str(property.get("value")))
    
    add_data(id, type, name, property_value[0], property_value[1], property_value[2], property_value[3], property_value[4], property_value[5], property_value[6], property_value[7])
    x+=1
print(x)


