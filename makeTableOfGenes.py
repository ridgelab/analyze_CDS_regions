#! /usr/bin/env python 3

'''
Makes a tab separated table of 
gene	species	assembly	sequence	transl_table
where the annotated gene has no exceptions and is not
a partial gene

Reads a directory of directories to find all assemblies
'''

import sys
import argparse
import gzip
import os


def parseArgs():
	'''
	Parses arguments. An input fasta file is required. 
	The number of cores is optional. By default, all available threads are used.
	An output file is optional. If an output file is not specified, output will be writted to standard out.
	'''
	parser = argparse.ArgumentParser(description='Find Orthologs in Two Files.')
	parser.add_argument("-i",help="Input Directory of Species Directories",action="store", dest="inputDir", required=True)
	parser.add_argument("-o",help="Output TSV table",action="store",dest="output", required=False)
	parser.add_argument("-z",help="View only gzipped files",action="store_true",dest="gzip", required=False)
	parser.add_argument("-oz",help="Output table as gzipped file",action="store_true",dest="output_gzip", required=False)
	#parser.add_argument("-t",help="Number of Cores",action="store",dest="threads",type=int, default=-1, required=False)
	args = parser.parse_args()

	if not os.path.isdir(args.inputDir):
		print (args.inputDir, "is not a valid directory!")
		sys.exit()
	return args



def readInputFiles(args):
	output = sys.stdout

	if args.output:
		if args.output_gzip:
			if args.output.endswith(".gz") or args.output.endswith(".gzip"):
				output = gzip.open(args.output,'w')
			else:
				output = gzip.open(args.output + ".gz",'w')

		else:
			output = open(args.output,'w')
	for path, subdirs, files in os.walk(args.inputDir):
		for name in files:
			file_path = os.path.join(path,name)
			inputFile = ""
			if args.gzip:
				if not file_path.endswith(".gz") and not file_path.endswith(".gzip"):
					continue
				inputFile = gzip.open(file_path)
			else:
				if file_path.endswith(".gz") or file_path.endswith(".gzip"):
					inputFile = gzip.open(file_path)
				else:
					inputFile = open(file_path)
			header = "start"
			while header != "": #Assumes fasta file has one-line sequences (as created in previous step)
				
				header = inputFile.readline()
				if isinstance(header,bytes):
					header=header.decode('UTF-8').strip()
				else:
					header=header.strip()
				if header == "":
					break
				print (header)
				seq = inputFile.readline()
				if isinstance(seq,bytes):
					seq=seq.decode('UTF-8').strip()
				else:
					seq=seq.strip()
				if 'exception' in header:
					continue
				if 'pseudo=true' in header:
					continue
				if 'transl_except' in header:
					continue
				if 'partial=true' in header:
					continue
				if "gene=" in header:
					geneName = header.split("gene=")[1].split(";")[0]
				else:
					geneName = header.split(">ID=")[1].split(";")[0]
				transl_table = header.split("transl_table=")[1]
				outputParams = [geneName.upper(),path.split("/")[-1],name.split(".g")[0],seq,transl_table] 
				if args.output_gzip:
					outputParams = [x.encode() for x in outputParams] 
					output.write(b"\t".join(outputParams) + b"\n")
				else:
					output.write("\t".join(outputParams) + "\n")
			inputFile.close()


if __name__ =='__main__':
	'''
	Main
	'''
	args = parseArgs()
	readInputFiles(args)

