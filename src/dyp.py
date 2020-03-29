from os import listdir, environ
from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
from os.path import getmtime
import sys, shutil, importlib

import graph_maker
import file_parser
import html.html_maker as hmaker
import html.html_writer as hwriter
import constants.platform_constants as pcsts
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

# returns a dictionary:
# absolute file name -> time_stamp
def read_cache(dest_dir):
	cache_name = join(dest_dir, '.cache', 'files.cache')
	if not isfile(cache_name):
		return {}
	
	info = {}
	f = open(cache_name, 'r')
	for line in f:
		abs_name, time_stamp = line.split(' ')
		info[abs_name] = str(time_stamp)[:-1]
	f.close()
	return info

def write_cache(dest_dir, all_info):
	cache_name = join(dest_dir, '.cache', 'files.cache')
	
	f = utils.make_file(cache_name)
	for abs_name in all_info:
		f.write(abs_name + ' ' + str(getmtime(abs_name)) + pcsts.nl)
	f.close()

def file_needs_html(cache, abs_name):
	# if file is not cached then needs parsing
	if abs_name not in cache:
		return True
	
	# if time stamp is different from the cached then needs parsing
	time_stamp = str(getmtime(abs_name))
	if time_stamp != cache[abs_name]:
		return True
	
	return False

def make_index_file(all_files, all_info):
	all_files = sorted(all_files)
	
	nl = pcsts.nl
	index = hwriter.html_writer(join(dest_dir, 'index.html'))
	index.start()
	index.open_head()
	index.put_meta({'charset' : 'UTF-8'})
	index.open_title()
	index.put(conf.PROJECT_NAME)
	index.close_tag()
	index.close_tag()
	
	index.open_body()
	index.open_h1()
	index.put(conf.PROJECT_NAME)
	index.close_tag()
	index.open_paragraph()
	index.put(conf.PROJECT_DESCRIPTION )
	index.close_tag()
	
	if conf.PROJECT_INCLUSION_GRAPH:
		index.add_image({'name' : 'project_graph.png', 'alt' : 'general_inclusion_map'})
	index.open_h2()
	index.put('Project files:')
	index.close_tag()
	
	index.open_unordered_list({'id' : 'project_files'})
	
	for f in all_files:
		index.open_list_element()
		index.open_paragraph()
		index.open_a({'href' : f})
		index.put(f)
		index.close_tag()
		index.close_tag()
		index.close_tag()
	
	index.close_tag()
	index.horizontal_line()
	index.open_paragraph()
	index.open_a({'href' : 'http://github.com/lluisalemanypuig/docyourprolog.git'})
	index.put('Generated with DYP')
	index.close_tag()
	index.close_tag()
	
	index.close_tag()
	index.close_tag()
	
	if conf.PROJECT_INCLUSION_GRAPH:
		graph_maker.make_full_graph(dest_dir, all_info, conf)

def print_usage():
	print("Document Your Prolog:")
	print("Generate html documentation to document your prolog code easily.")
	print()
	print("    [-h, --help]")
	print("        Prints the usage and exits.")
	print()
	print("    [-c, --config-file] FILE")
	print("        Tell what configuration should be used to generate the")
	print("        documentation. The name of the file can be absoulte or")
	print("        relative, but it must not contain the extension .py")
	print()
	print("    [-g, --gen-config] FILE")
	print("        Generate a new configuration file.")
	print("        FILE is the name of the new generated file.")


# ****************************
# *                          *
# *        Start code        *
# *                          *
# ****************************

# Initialise platform-dependent constants
pcsts.make_constants()

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
		print("Error: unrecognised option '%s'" % argv[i])
		exit(1)
	i += 1

if config_from == None and config_to == None:
	print("Error: this program needs either the configuration to be read")
	print("    or where to generate a new configuration file.")
	print_usage()
	exit(1)

if config_from != None and config_to != None:
	print("Error: specify only the configuration file to be read or where")
	print("    to generate a new configuration file, but not both.")
	print_usage()
	exit(1)

# start making documentation (or file configuration)

mypath, myexe = utils.abspath_name(argv[0])
def_config_file = join(mypath, "config")
sys.path.append(def_config_file)
conf = importlib.import_module("default_config")
environ['PATH'] += ":" + conf.DOT_EXE_PATH

if config_to != None:
	print("Generating default configuration file...")
	shutil.copyfile(def_config_file + "/default_config.py", config_to)
	exit(0)

if config_from != None:
	print("Reading configuration file:", config_from)
	abs_path, name = utils.abspath_name(config_from)
	sys.path.append(abs_path)
	del conf
	conf = importlib.import_module(name)

source_dir = conf.SRC_DIR
dest_dir = conf.DEST_DIR
exts = conf.EXTENSIONS

print("    source dir:", source_dir)
print("    destination dir:", dest_dir)
print("    extensions to be parsed:", exts)

# read cache from cache file
cache = read_cache(dest_dir)

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

print("Parsing source files:")

while len(to_be_parsed) > 0:
	abs_name = to_be_parsed[0]
	del to_be_parsed[0]
	
	if abs_name not in already_parsed:
		rel_name = relpath(abs_name, source_dir)
		path_to_file, name_file = utils.abspath_name(abs_name)
		
		print("    >> Parsing:", rel_name)
		
		# parse file
		information = file_parser.file_parser(source_dir, abs_name)	
		
		information.parse_file()
		information.make_extra_names(dest_dir)
		# store information parsed
		all_info[abs_name] = information
		already_parsed.add(abs_name)
		
		# include next files to be parsed
		if conf.FOLLOW_INCLUDES:
			to_be_parsed += information.get_included_files()
		
		class_blocks = information.get_class_blocks()

print()
print("Making html files:")

some_html_generated = False
all_files = []
for abs_name, info in all_info.items():
	
	# check that file needs to be parsed again
	if file_needs_html(cache, abs_name):
		some_html_generated = True
		
		print("    >> Making html file for:", info.get_rel_name())
		
		maker = hmaker.html_maker(conf, source_dir, all_info, info)
		maker.make_html_file()
		
		if conf.FILE_INCLUSION_GRAPH and info.needs_inc_graph():
			graph_maker.make_single_graph(dest_dir, info, all_info, conf)
	else:
		print("    >> Html file for", info.get_rel_name(), "-- already made")
		
	rel_name = info.get_rel_html_name()
	all_files.append(rel_name)

if some_html_generated:
	# make html for index if necessary
	print("    >> Making html file for index")
	make_index_file(all_files, all_info)
	
	# rewrite cache file, if necessary
	if conf.CACHE_FILES:
		write_cache(dest_dir, all_info)

