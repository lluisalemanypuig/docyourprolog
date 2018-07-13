import argparse
import os
import file_parser

def path_and_name(filename):
	abs_path = os.path.abspath(filename)
	path_to_dir = os.path.dirname(abs_path)
	s = len(filename) - 1
	while s > 0 and filename[s] != '/': s -= 1
	name = filename[(s+1):]
	return (path_to_dir, name)

def absolute_filename(filename):
	path, name = path_and_name(filename)
	return path + "/" + name

parser = argparse.ArgumentParser(description="Document your Prolog")
parser.add_argument('-m', '--main', type=str, help='Main file of the project',)
parser.add_argument('-d', '--src-dir', type=str, help='Directory with all the sources')
parser.add_argument('-r', '--recursive', type=bool, help='Parse source directory recursively')
args = parser.parse_args()

# split main file into path and name
path, name = path_and_name(args.main)

# files to be parsed
to_be_parsed = [ path + "/" + name ]
# files already parsed
already_parsed = set([])
# objects with 
information = []

while len(to_be_parsed) > 0:
	filename = to_be_parsed[0]
	del to_be_parsed[0]
	
	abs_fname = absolute_filename(filename)
	
	if abs_fname not in already_parsed:
		print ">> Parsing:", filename
		# parse file, store information parsed
		information = file_parser.file_parser(filename)
		already_parsed.add(abs_fname)
		
		# split file name into subpath and name
		subpath, _ = path_and_name(filename)
		# include next files to be parsed
		for name in information.get_included_files():
			to_be_parsed += [subpath + "/" + name]
	


