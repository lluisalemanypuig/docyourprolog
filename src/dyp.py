from os import listdir, environ
from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
import sys, shutil, importlib

import graph_maker
import file_parser
import html_maker as hmaker
import constants
import utils

def get_matching_files(dirname, patterns, rec):
	files = []
	dirs = []
	this_dir = listdir(dirname)
	for f in this_dir:
		abs_name = join(dirname, f)
		abs_name = utils.resolve_path(abs_name)
		
		if isfile(abs_name):
			extension = splitext(f)[1]
			if extension in patterns:
				files.append(abs_name)
		else: 
			dirs.append(f)
	
	if rec:
		for d in dirs:
			abs_path = join(dirname, d)
			abs_path = utils.resolve_path(abs_path)
			
			files += get_matching_files(abs_path, patterns, rec)
	
	return files

def print_usage():
	print "Document Your Prolog:"
	print "Generate html documentation to document your prolog code easily."
	print
	print "    [-h, --help]             Prints the usage and exits."
	print "    [-c, --config-file] FILE The configuration file containing the"
	print "                             configuration for the documentation."
	print "    [-g, --gen-config] FILE  Directory where to generate an empty"
	print "                             configuration file."
	
# **********
# Start code
# **********

# Initialise platform-dependent constants
constants.make_constants()

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
	print_usage()
	exit(1)

if config_from != None and config_to != None:
	print "Error: specify only the configuration file to be read or where"
	print "    to generate a new configuration file, but not both."
	exit(1)

mypath, myexe = utils.abspath_name(argv[0])
def_config_file = join(mypath, "config")
sys.path.append(def_config_file)
conf = importlib.import_module("default_config")
environ['PATH'] += ":" + conf.DOT_EXE_PATH

if config_to != None:
	shutil.copyfile(def_config_file + "/default_config.py", config_to)
	exit(0)

if config_from != None:
	abs_path, name = utils.abspath_name(config_from)
	sys.path.append(abs_path)
	del conf
	conf = importlib.import_module(name)

source_dir = conf.SRC_DIR
dest_dir = conf.DEST_DIR
exts = conf.EXTENSIONS

# files to be parsed
to_be_parsed = []
path = None

# parse all files inside source_dir
source_dir = abspath(source_dir)
dest_dir = dest_dir

names = get_matching_files(source_dir, exts, conf.RECURSIVE)
for name in names:
	to_be_parsed.append( join(source_dir, name) )

# files already parsed
already_parsed = set([])
# relate each file's full path to its file parser object
all_info = {}

print "Parsing source files:"

while len(to_be_parsed) > 0:
	abs_path = to_be_parsed[0]
	del to_be_parsed[0]
	
	if abs_path not in already_parsed:
		rel_name = relpath(abs_path, source_dir)
		path_to_file, name_file = utils.abspath_name(abs_path)
		
		print ">> Parsing:", rel_name
		
		# parse file
		information = file_parser.file_parser(source_dir, abs_path)
		information.make_extra_names(dest_dir)
		# store information parsed
		all_info[abs_path] = information
		already_parsed.add(abs_path)
		
		# include next files to be parsed
		if conf.FOLLOW_INCLUDES:
			to_be_parsed += information.get_included_files()

print
print "Making html files:"

all_files = []
for abs_path, info in all_info.iteritems():
	print ">> Making html file for:", info.get_rel_name()
	
	print "   ", info.get_abs_html_name()
	print "   ", info.get_abs_html_path()
	print "   ", info.get_rel_html_name()
	print "   ", info.get_rel_html_path()
	
	maker = hmaker.html_maker(conf, source_dir, all_info, info)
	maker.make_html_file()
	
	if conf.FILE_INCLUSION_GRAPH and info.needs_inc_graph():
		print "    + Make graph file"
		graph_maker.make_single_graph(dest_dir, info, all_info, conf)
	
	rel_name = info.get_rel_html_name()
	all_files.append(rel_name)

print ">> Making html file for index"
all_files = sorted(all_files)

nl = constants.nl
html_index = utils.make_file(join(dest_dir, 'index.html'))
html_index.write("<html>" + nl)

html_index.write("<head>" + nl)
html_index.write("<title>" + conf.PROJECT_NAME + "</title>" + nl)
html_index.write("</head>" + nl)
html_index.write("<body>" + nl)
html_index.write("<h1>" + conf.PROJECT_NAME + "</h1>" + nl)
html_index.write("<p>" + conf.PROJECT_DESCRIPTION + "</p>" + nl)
if conf.PROJECT_INCLUSION_GRAPH:
	html_index.write("<img src=\"project_graph.png\" alt=\"general_inlusion_map\">" + nl)
html_index.write("<h2>Project files:</h2>" + nl)
html_index.write("<ul id=\"project_files\">" + nl)
file_list_item = "<li><p><a href=\"%s\">%s</a></p></li>"

for f in all_files:
	html_index.write((file_list_item % (f, f)) + nl)

html_index.write("</ul>" + nl)
html_index.write(constants.html_git_footer)
html_index.write("</body>" + nl)
html_index.write("</html>" + nl)
html_index.close()

if conf.PROJECT_INCLUSION_GRAPH:
	print "    + Make graph file"
	graph_maker.make_full_graph(dest_dir, all_info, conf)
