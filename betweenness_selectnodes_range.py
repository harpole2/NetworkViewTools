import argparse
import numpy as np
import networkx as nx
from pprint import pprint
import sys


def main(argv):
    loadData(argv)
    getNodeSpecBetweenness()

def loadData(argv):
    global outfile
    global data
    global sources
    global sinks
    parser = argparse.ArgumentParser(description='Compute betweenness for a subset of sources and target')
    parser.add_argument('-c','--contact',help='contact matrix (usually contact.dat)', required=True)
    parser.add_argument('-o','--output',help='output prefix', required=True)
    parser.add_argument('-ss','--Startsources',help='First Residue in Sources',type=int, required=True)
    parser.add_argument('-es','--Endsources',help='Last Residue in Sources (it includes this residue)',type=int, required=True)
    parser.add_argument('-st','--Starttargets',help='First Residue in Target',type=int, required=True)
    parser.add_argument('-et','--Endtargets',help='Last Residue in Target (it includes this residue)',type=int, required=True)

    args = vars(parser.parse_args())
    contactPrefix=args['contact']
    outfile=args['output']
    ssources=args['Startsources']
    esources=args['Endsources']
    ssinks=args['Starttargets']
    esinks=args['Endtargets']
    sources=range(ssources,esources+1)
    sinks=range(ssinks,esinks+1)
    print sources

    data = np.genfromtxt(contactPrefix,skip_header=1)




def getNodeSpecBetweenness():
    global outfile
    global data
    global sources
    global sinks
    weight = []
    G=nx.from_numpy_matrix(data)
    for i in xrange(len(data)):
        for j in xrange(i+1,len(data)):
            if(data[i,j] != 0):
                weight.append(data[i,j])

    G=nx.from_numpy_matrix(data)
    net=nx.betweenness_centrality_subset(G,sources=sources,targets=sinks,normalized=False,weight="weight")
    f=open(outfile, 'w')
    with open(outfile, 'w') as f:
        for key, value in net.items():
            f.write('%s %s\n' % (key, value))

if __name__ == "__main__":
    main(sys.argv[1:])
