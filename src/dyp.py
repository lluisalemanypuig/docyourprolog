from sys import argv
from os import listdir
from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
import file_parser
import constants
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
	print "Generate html documentation to document your prolog code easily."
	print
	print "    [-h, --help]            Prints the usage and exits"
	print "    [-s, --source-dir] DIR  Indicates the source_dir to be parsed"
	print "    [-d, --dest-dir] DIR    Where to store the html files"
	print "    [-r, --recursive]       Iterate recursively on all directories found in"
	print "                            main source_dir and parse the files found"
	print "    [-e, --extension] LIST  Parse only those files whose extension matches"
	print "                            one of the extensions in LIST."
	print "                            Default: \"['.pl','.prolog']\""
	
# **********
# Start code
# **********

# Parse arguments

source_dir = None
dest_dir = None
recursive = False
exts = [".pl", ".prolog"]
i = 1
while i < len(argv):
	if argv[i] == "-h" or argv[i] == "--help":
		print_usage()
		exit(0)
	elif argv[i] == "-s" or argv[i] == "--source-dir":
		source_dir = argv[i + 1]
		i += 1
	elif argv[i] == "-d" or argv[i] == "--dest-dir":
		dest_dir = argv[i + 1]
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

if source_dir == None:
	print "Error: the source_dir containing the files must be specified"
	print
	print_usage()
	exit(1)
if dest_dir == None:
	print "Error: the dest_dir specifying where to store the html files must be specified"
	print
	print_usage()
	exit(1)

# Initialise platform-dependent constants
constants.make_constants()

# files to be parsed
to_be_parsed = []
path = None

# parse all files inside source_dir
source_dir = abspath(source_dir)
dest_dir = abspath(dest_dir)
names = get_matching_files(source_dir, exts, recursive)
for name in names:
	to_be_parsed.append( join(source_dir, name) )

# files already parsed
already_parsed = set([])
# relate each file's full path to its information object
file_info = {}

while len(to_be_parsed) > 0:
	abs_path = to_be_parsed[0]
	del to_be_parsed[0]
	
	if abs_path not in already_parsed:
		relative_name = relpath(abs_path, source_dir)
		path_to_file, name_file = utils.abspath_name(abs_path)
		
		print ">> Parsing:", relative_name
		
		# parse file
		information = file_parser.file_parser(abs_path)
		# set relative and short names
		information.set_relative_name(relative_name)
		information.set_short_name(name_file)
		information.make_html_names(dest_dir)
		# store information parsed
		file_info[abs_path] = information
		already_parsed.add(abs_path)
		
		# include next files to be parsed
		for name in information.get_included_files():
			to_be_parsed += [path_to_file + "/" + name]

for abs_path, info in file_info.iteritems():
	print abs_path
	print "    prolog:", info.get_abs_name()
	print "    prolog:", info.get_relative_name()
	print "    prolog:", info.get_short_name()
	print "      html:", info.get_abs_html()
	print "      html:", info.get_relative_html()
	print "      html:", info.get_short_html()
	"""
	for B in info.get_blocks():
		if B.block_info() != None:
			B.block_info().show("    ")
	"""
	print
	#info.make_html_file()
