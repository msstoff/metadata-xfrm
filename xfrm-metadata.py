#! /user/bin/python3

'''
This script transforms the output from a metadata dependency query into gefx -
suitable for loading into gephi for graphing.
'''
from collections import namedtuple
import string
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump, tostring
import argparse

# list to hold parsed records
recList = []

# dictionary to store nodes
nodeDict = {}

# named tuple to structure data
MetadataRecord = namedtuple('MetadataRecord', ['compId', 'compName', 'compType', 'refId', 'refName', 'refType'])

# empty ElementTree
tree = ElementTree()

# parse command line arguments
def parseArgs() :
    parser = argparse.ArgumentParser(description='Transforms a metadata query file into gexf output for graphing.')
    parser.add_argument( 'infile', help='The metadata file to be read')
    parser.add_argument('outfile', help="The transformed gexf file")
    parser.add_argument('-t', '--tests', help='Include test classes', action='store_true')
    args = parser.parse_args()
    return args

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
    if mRec.compId not in nodeDict:
        if args.tests:
            nodeDict[mRec.compId] = mRec.compName
        else:
            if 'Test' not in mRec.compName:
                nodeDict[mRec.compId] = mRec.compName


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


#  iterate list & write nodes using the dictionary
def createNodes(graph) :
    nodes = SubElement(graph, "nodes")
    for compId, compName in nodeDict.items() :
        aNode = SubElement(nodes, "node", id=compId, label=compName)
    print('Created nodes: ', len(nodeDict))

#  iterate list & write edges
def createEdges(graph) :
    edges = SubElement(graph, "edges")
    edgeCount = 0
    for rec in recList:
        # filter edges if both endpoints are not in nodeDict
        if (rec.compId in nodeDict) and (rec.refId in nodeDict):
            edgeCount += 1
            idx = rec.compId[-8:] + rec.refId[-8:]
            anEdge = SubElement(edges, "edge", id=idx, source=rec.compId, target=rec.refId)
    print('Created edges: ', edgeCount)



'''
Main execution
'''
args = parseArgs()
datafile = args.infile
gexfFile = args.outfile

# check the file exists & open
with open(datafile ) as f:
    header=f.readline()
    separator=f.readline()
    recCount = 0
    for line in f:
        if not line.startswith('Total'):
            recCount += 1
            parseLine(line)
f.close()

print('Input lines read: ', recCount)

graph = initializeTree(tree)

createNodes(graph)
createEdges(graph)

# write out xml
tree.write(gexfFile, encoding='UTF-8', xml_declaration=True)