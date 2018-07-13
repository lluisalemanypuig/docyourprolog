from sys import argv
from os import listdir
from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
import file_parser
import utils

def get_matching_files(dirname, pats, rec):
	files = []
	dirs = []
	this_dir = listdir(dirname)
	for f in this_dir:
		full_name = join(dirname, f)
		if isfile(full_name):
			extension = splitext(f)[1]
			if extension in pats:
				files.append(full_name)
		else: 
			dirs.append(f)
	
	if rec:
		for d in dirs:
			full_dir = join(dirname, d)
			files += get_matching_files(full_dir, pats, rec)
	
	return files

def print_usage():
	print "Document Your Prolog:"

# **********
# Start code
# **********

# Parse arguments

main_dir = None
recursive = False
exts = [".pl", ".prolog"]
i = 1
while i < len(argv):
	if argv[i] == "-h" or argv[i] == "--help":
		print_usage()
		exit(0)
	elif argv[i] == "-d" or argv[i] == "--main-dir":
		main_dir = argv[i + 1]
		i += 1
	elif argv[i] == "-r" or argv[i] == "--recursive":
		recursive = True
	elif argv[i] == "-e" or argv[i] == "--extension":
		exts = eval(argv[i + 1])
		i += 1
	else:
		print "Error: unrecognised option '%s'" % argv[i]
		exit(1)
	i += 1

if main_dir == None:
	print "Error: the directory containing the files must be specified"
	exit(1)

# files to be parsed
to_be_parsed = []
path = None

# parse all files inside directory
directory = abspath(main_dir)
print "directory:", directory
names = get_matching_files(directory, exts, recursive)
for name in names:
	to_be_parsed.append( join(directory, name) )

# files already parsed
already_parsed = set([])
# relate each file's full path to its information object
file_info = {}

while len(to_be_parsed) > 0:
	abs_path = to_be_parsed[0]
	del to_be_parsed[0]
	
	if abs_path not in already_parsed:
		print ">> Parsing:", abs_path
		
		# parse file
		information = file_parser.file_parser(abs_path)
		# set relative and short names
		relative_name = relpath(abs_path, directory)
		path_to_file, name_file = utils.path_and_name(abs_path)
		information.set_relative_name(relative_name)
		information.set_short_name(name_file)
		# store information parsed
		file_info[abs_path] = information
		already_parsed.add(abs_path)
		
		# include next files to be parsed
		for name in information.get_included_files():
			to_be_parsed += [path_to_file + "/" + name]

print file_info

for abs_path, info in file_info.iteritems():
	print abs_path
	print "    ", info.get_abs_name()
	print "    ", info.get_relative_name()
	print "    ", info.get_short_name()


