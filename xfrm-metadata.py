#! /user/bin/python3

'''
This script transforms the output from a metadata dependency query into gefx -
suitable for loading into gephi for graphing.
'''
from collections 
import namedtuple
import string
from xml.etree.ElementTree import ElementTree, Element, SubElement, dump, tostring
import argparse

# list to hold parsed records
recList = []

# named tuple to structure data
MetadataRecord = namedtuple('MetadataRecord', ['compId', 'compName', 'compType', 'refId', 'refName', 'refType'])

# empty ElementTree
tree = ElementTree()

# set default file names for testing
datafile = './apex.txt' 
gexfFile = './apex.gexf'

# parse command line arguments
def parseArgs() :
    parser = argparse.ArgumentParser(description='Transforms a metadata query file into gexf output for graphing.')
    parser.add_argument( 'infile', help='The metadata file to be read')
    parser.add_argument('outfile', help="The transformed gexf file")
    parser.add_argument('-t', '--tests', help='Include test classes', action='store_true')
    args = parser.parse_args()
    return args

# parse line, create tuple, & write to list
# TODO: check for test flag
# TODO: check line for 'Test' in compName or refName
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
args = parseArgs()
datafile = args.infile
gexfFile = args.outfile
print('datafile: ', datafile)
print('gexfFile: ', gexfFile)

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
tree.write(gexfFile, encoding='UTF-8', xml_declaration=True)