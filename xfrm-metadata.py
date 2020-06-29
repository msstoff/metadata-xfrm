#! /user/bin/python3

'''
This script transforms the output from a metadata dependency query into gefx -
suitable for loading into gephi for graphing.
'''
from collections import namedtuple
import string
from xml.etree.ElementTree import Element, SubElement, dump

# list to hold parsed records
recList = []
# named tuple to structue data
MetadataRecord = namedtuple('MetadataRecord', ['compId', 'compName', 'compType', 'refId', 'refName', 'refType'])
# empty Element root
root = Element("{http://www.gephi.org/gexf}gexf")

# get command line parameters e.g. file name
datafile = './apex.txt'  # set a name for testing

# parse fixed length record, create tuple, & write to list
def parseLine(line) :
    mRec = MetadataRecord(  
                            compId = line[0:18],
                            compName = line[21:54].strip(),
                            compType = line[56:77].strip(),
                            refId = line[79:97],
                            refName = line[103:134].strip(),
                            refType = line[136:158].strip()
                        )
    recList.append(mRec)


# initialize output xml
def initializeTree(root) :
    graph = SubElement(root, "graph", type = "static")

    attr = SubElement(graph, "attributes")
    attr.attrib["class"] = "node"
    attr.attrib["type"] = "static"
    attrib = SubElement(attr, "attribute", id="label", title="label", type="string")
    return graph


#  iterate list & write nodes
def createNodes(recList, graph) :
    nodes = SubElement(graph, "nodes")
    for rec in recList:
        aNode = SubElement(nodes, "node", id=rec.compId, label=rec.compName)

#  iterate list & write edges
def createEdges(recList, graph) :
    edges = SubElement(graph, "edges")
    for rec in recList:
        idx = rec.compId[-8:] + rec.refId[-8:]
        anEdge = SubElement(edges, "edge", id=idx, source=rec.compId, target=rec.refId)



'''
Main execution
'''

# check the file exists & open
with open(datafile ) as f:
    header=f.readline()
    separator=f.readline()
    for line in f:
        if not line.startswith('Total'):
            parseLine(line)
f.close()

graph = initializeTree(root)

createNodes(recList, graph)

createEdges(recList, graph)

# write out xml

dump(root)