import argparse
import numpy as np
import networkx as nx
from pprint import pprint
import mdtraj as md
import sys


def main(argv):
    loadData(argv)
    getNodeSpecBetweenness()

def loadData(argv):
    global outfile
    global data
    global source
    global sink
    global distance
    global dist_mat
    parser = argparse.ArgumentParser(description='Compute betweenness for a subset of sources and target')
    parser.add_argument('-c','--contact',help='contact matrix (usually contact.dat)', required=True)
    parser.add_argument('-m','--matrix',help='distance matrix (still need to explain format)', required=True)
    parser.add_argument('-o','--output',help='output prefix', required=True)
    parser.add_argument('-s','--source',help='Single Residue to Exapnd Source around',type=int, required=True)
    parser.add_argument('-t','--target',help='Single residue to Expand Target around',type=int, required=True)
    parser.add_argument('-d','--distance',help='Distance from Calpha(or potentially sidechain) (USE SAME UNITS AS DISTANCE MATRIX) for picking residues in Source and Target',type=float, required=True)

    args = vars(parser.parse_args())
    contactPrefix=args['contact']
    distmat=args['matrix']
    outfile=args['output']
    source=args['source']
    sink=args['target']
    distance=args['distance'] 
    data = np.genfromtxt(contactPrefix,skip_header=1)
    dist_mat = np.genfromtxt(distmat)




def getNodeSpecBetweenness():
    global outfile
    global data
    global source
    global sink
    global distance
    global dist_mat
    weight = []
    sources=[]
    sinks=[]
    sinks.append(sink)
    for i in range(0,len(dist_mat[source])):
      if dist_mat[source,i] <= distance:
        sources.append(i)
    print "sources are: ",sources
    print "sinks are: ",sinks
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
