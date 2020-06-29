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
        compId=line[0:18]
        compName=line[21:54].strip()
        compType=line[56:77].strip()
        refId=line[79:97]
        refName=line[103:134].strip()
        refType=line[136:158].strip()
        print('node: ', compId, compName, compType, refId, refName, refType)


