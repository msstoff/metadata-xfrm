#! /user/bin/python3

'''
This script transforms the output from a metadata dependency query into gefx -
suitable for loading into gephi for graphing.
'''
from collections import namedtuple
import string
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump, tostring

# list to hold parsed records
recList = []

# named tuple to structure data
MetadataRecord = namedtuple('MetadataRecord', ['compId', 'compName', 'compType', 'refId', 'refName', 'refType'])

# empty ElementTree
tree = ElementTree()


# get command line parameters e.g. file name
datafile = '/Users/mstofferahn/Downloads/xref.txt'  # set a name for testing
outFile = '/Users/mstofferahn/Downloads/xref.gexf'

# parse line, create tuple, & write to list
def parseLine(line) :
    splitLine = line.split()
    mRec = MetadataRecord(  
        compId=splitLine[0],
        compName=splitLine[1],
        compType=splitLine[2],
        refId=splitLine[3],
        refName=splitLine[4],
        refType=splitLine[5]
        )
    recList.append(mRec)


# initialize output xml
def initializeTree(tree) :
    root = Element("gexf")
    root.set('xmlns', 'http://www.gexf.net/1.3')
    root.set('version', '1.3')
    root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:schemaLocation','http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd')
    tree._setroot(root)
    graph = SubElement(root, "graph")
    graph.set('defaultedgetype','directed')
    graph.set('mode','static')
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

graph = initializeTree(tree)

createNodes(recList, graph)

createEdges(recList, graph)

# write out xml
tree.write(outFile, encoding='UTF-8', xml_declaration=True)