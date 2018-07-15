from os import listdir
from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
import sys, shutil, importlib

import file_parser
import html_maker as hmaker
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
	print "    [-h, --help]             Prints the usage and exits."
	print "    [-c, --config-file] FILE Indicates the configuration file that"
	print "                             should be used to make the documentation."
	print "    [-g, --gen-config] FILE  Where to generate an empty configuration"
	print "                             file."
	
# **********
# Start code
# **********

# Parse arguments

argv = sys.argv
config_from = None
config_to = None
i = 1
while i < len(argv):
	if argv[i] == "-h" or argv[i] == "--help":
		print_usage()
		exit(0)
	elif argv[i] == "-c" or argv[i] == "--config-file":
		config_from = argv[i + 1]
		i += 1
	elif argv[i] == "-g" or argv[i] == "--gen-config":
		config_to = argv[i + 1]
		i += 1
	else:
		print "Error: unrecognised option '%s'" % argv[i]
		exit(1)
	i += 1

if config_from == None and config_to == None:
	print "Error: this program needs either the configuration to be read"
	print "    or where to generate a new configuration file."
	usage()
	exit(1)

if config_from != None and config_to != None:
	print "Error: specify only the configuration file to be read or where"
	print "    to generate a new configuration file, but not both."
	exit(1)

mypath, myexe = utils.abspath_name(argv[0])
sys.path.append(join(mypath, "config"))
conf = importlib.import_module("default_config")

if config_to != None:
	shutil.copyfile("config/default_config.py", config_to)
	exit(0)

if config_from != None:
	abs_path, name = utils.abspath_name(config_from)
	sys.path.append(abs_path)
	del conf
	conf = importlib.import_module(name)

source_dir = conf.SRC_DIR
dest_dir = conf.DEST_DIR
exts = conf.EXTENSIONS

# Initialise platform-dependent constants
constants.make_constants()

# files to be parsed
to_be_parsed = []
path = None

# parse all files inside source_dir
source_dir = abspath(source_dir)
dest_dir = dest_dir

print "source:", source_dir
print "  dest:", dest_dir

names = get_matching_files(source_dir, exts, conf.RECURSIVE)
for name in names:
	to_be_parsed.append( join(source_dir, name) )

# files already parsed
already_parsed = set([])
# relate each file's full path to its information object
all_info = {}

while len(to_be_parsed) > 0:
	abs_path = to_be_parsed[0]
	del to_be_parsed[0]
	
	if abs_path not in already_parsed:
		rel_name = relpath(abs_path, source_dir)
		path_to_file, name_file = utils.abspath_name(abs_path)
		
		print ">> Parsing:", rel_name
		
		# parse file
		information = file_parser.file_parser(source_dir, abs_path)
		information.make_html_names(dest_dir)
		# store information parsed
		all_info[abs_path] = information
		already_parsed.add(abs_path)
		
		# include next files to be parsed
		to_be_parsed +=  information.get_included_files()

for abs_path, info in all_info.iteritems():
	print abs_path
	print "    File paths:"
	print "        prolog absolute name:", info.get_abs_name()
	print "        prolog absolute path:", info.get_abs_path()
	print "        prolog relative name:", info.get_rel_name()
	print "        prolog relative path:", info.get_rel_path()
	print "           prolog short name:", info.get_short_name()
	print "          html absolute name:", info.get_abs_html_name()
	print "          html absolute path:", info.get_abs_html_path()
	print "          html relative name:", info.get_rel_html_name()
	print "          html relative path:", info.get_rel_html_path()
	print "             html short name:", info.get_short_html_name()
	print "              included files:", info.get_included_files()
	for btype, block_list in info.get_class_blocks().iteritems():
		for B in block_list:
			if B != None:
				B.show("    ")
	print
	maker = hmaker.html_maker(source_dir, all_info, info)
	maker.make_html_file()
