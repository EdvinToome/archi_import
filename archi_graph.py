import xml.etree.ElementTree as ET
import re
import sys
import mariadb

def get_all_children(children, element):
    for child in element:
        if(re.search("^archimate" ,str(child.get("{http://www.w3.org/2001/XMLSchema-instance}type")))):
            children.append(child)
        if(len(child) > 0):
            get_all_children(children, child)
    return children

def add_data(source, target):
#    print(sid,type,name,ipv4,os,vpc,stage,eol)
    try: 
        cur.execute("INSERT INTO archi_graph (source, target) VALUES (?, ?)", (source, target)) 
    except mariadb.Error as e: 
        print(f"Error adding data to MariaDB: {e}")
    conn.commit() 

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
cur = conn.cursor()
tree = ET.parse('eits_demo.archimate')
root = tree.getroot()
children = []
children = get_all_children(children, root)
for child in children:
    type = str(child.get("{http://www.w3.org/2001/XMLSchema-instance}type"))
    if type == "archimate:RealizationRelationship" or type == "archimate:AssignmentRelationship" or type == "archimate:ServingRelationship" or type == "archimate:AssociationRelationship": 
        source = child.get("source")
        target = child.get("target")
        add_data(source, target)


