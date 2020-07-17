#! /user/bin/python3

# Load fixed width file
import string

# get file name to import
datafile = './apex.txt'

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