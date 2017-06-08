import argparse
import numpy as np
import sys
import os.path

def main(argv):
	loadData(argv)
	makecut()

def loadData(argv):
	global diction
	global outfile
	global cut
	parser = argparse.ArgumentParser(description='Culls Network node inclusion based on cutoff')
	parser.add_argument('-i','--inputfile',help='input file to be culled', required=True)
	parser.add_argument('-o','--output',help='output file', required=True)
	parser.add_argument('-c','--cutoff',help='remove values below this', type=float, required=True)

	args = vars(parser.parse_args())
	infile=args['inputfile']
	outfile=args['output']
	cut = args['cutoff']

	diction={}
	with open(infile, 'r') as f:
		for line in f:
			(key,val)= line.split()
			diction[key]=val


def makecut():
	global diction
	global outfile
	global cut



	f2=open(outfile, 'w')
	with open(outfile, 'w') as f2:
		for key, value in sorted(diction.iteritems(), key=lambda t: t[0]):
			if float(value) > cut:
				f2.write('%s %s\n' % (key, value))

	root = os.path.splitext(outfile)[0]
	outfile2=root+'_res_VMD.dat'
	f3=open(outfile2, 'w')
	with open(outfile2, 'w') as f3:
		for key, value in sorted(diction.iteritems(), key=lambda t: t[0]):
			if float(value) > cut:
				f3.write('%s ' % key)

if __name__ == "__main__":
	main(sys.argv[1:])
