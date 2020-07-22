#! /user/bin/python3

# Load fixed width file
import string
import argparse

# get file name to import
parser = argparse.ArgumentParser(description='Read a file')
parser.add_argument( 'infile', help='The metadata file to be read')
parser.add_argument('-o','--outfile', help="The transformed gexf file")
parser.add_argument('-t', '--tests', help='Include test classes', action='store_true')
args = parser.parse_args()

datafile = args.infile

print(args.infile)
if (args.tests) :
    print('Tests has been set')
else :
    print('Tests is not set')
if args.outfile :
    print('outfile is set to', args.outfile)

# load file & create tuples

with open(datafile ) as f:
    header=f.readline()
    separator=f.readline()
    for line in f:
        splitLine = line.split()
        compId=splitLine[0]
        compName=splitLine[1]
        compType=splitLine[2]
        refId=splitLine[3]
        refName=splitLine[4]
        refType=splitLine[5]
        print('node: ', compId, compName, compType, refId, refName, refType)