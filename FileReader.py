# Load fixed width file
import string

# get file name to import
datafile = './apex.txt'

# load file & create tuples

with open(datafile ) as f:
    header=f.readline()
    separator=f.readline()
    for line in f:
        compid=line[0:18]
        compname=line[21:54]
        print('node: ', compid, compname.strip())

# initialize output xml

# write nodes 

# write edges


