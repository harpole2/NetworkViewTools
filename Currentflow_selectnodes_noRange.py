import argparse
import numpy as np
import networkx as nx
from pprint import pprint
import sys
import os.path


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
	parser.add_argument('-s','--sources',nargs='+',help='list of source residues',type=int, required=True)
	parser.add_argument('-t','--targets',nargs='+',help='list of target residues',type=int, required=True)

	args = vars(parser.parse_args())
	contactPrefix=args['contact']
	outfile=args['output']
	sources=args['sources']
	sinks=args['targets']
	data = np.genfromtxt(contactPrefix,skip_header=1)




def getNodeSpecBetweenness():
	global outfile
	global data
	global sources
	print sources
	global sinks
	print sinks
	weight = []
	G=nx.from_numpy_matrix(data)
	for i in xrange(len(data)):
		for j in xrange(i,len(data)):
			if(data[i,j] != 0):
				weight.append(data[i,j])

	net=nx.current_flow_betweenness_centrality_subset(G,sources=sources,targets=sinks,normalized=False,weight="weight")
	f=open(outfile, 'w')
	with open(outfile, 'w') as f:
		for key, value in net.items():
			if value > 0.0:
				f.write('%s %s\n' % (key, value))
	root = os.path.splitext(outfile)[0]
	outfile2=root+'_res_VMD.dat'
	f2=open(outfile2, 'w')
	with open(outfile2, 'w') as f2:
		for key, value in net.items():
			if value > 0.0:
				f2.write('%s ' % key)

if __name__ == "__main__":
	main(sys.argv[1:])
