from os.path import join, relpath
import os

import file_parser
import constants
import utils

# adds all edges to files incldued in abs_name
def make_one_level(dot_file, abs_name, top_rel_path, all_info):
	nl = constants.nl
	
	if abs_name not in all_info:
		return []
	
	fp = all_info[abs_name]
	inc_files = fp.get_included_files()
	pl_rel_inc_files = []
	
	my_short_name_pl = fp.get_short_name()
	my_rel_name_dot = fp.get_rel_dot_name()
	
	for f in inc_files:
		their_rel_pl_name = all_info[f].get_rel_name()
		pl_name_href = relpath(their_rel_pl_name, top_rel_path)
		pl_rel_inc_files.append(pl_name_href)
		
		dot_file.write("\"" + pl_name_href + "\" [shape=square]" + nl)
		dot_file.write("\"" + my_short_name_pl + "\" -> \"" + pl_name_href + "\"" + nl)
	
	return inc_files

# makes the graph for all parsed files in all_info
def make_full_graph(dest_dir, all_info):
	print "hey"

# makes the graph for the parsed file 'fp'
def make_single_graph(dest_dir, fp, all_info):
	nl = constants.nl
	
	top_rel_path = fp.get_rel_path()
	my_short_name_pl = fp.get_short_name()
	my_rel_name_dot = fp.get_rel_dot_name()
	my_rel_name_png = fp.get_rel_png_name()
	
	print "Create:", join(dest_dir, my_rel_name_dot)
	print "  my pl label:", my_short_name_pl
	
	dot_file = utils.make_file(join(dest_dir, my_rel_name_dot))
	dot_file.write("digraph file_graph {" + nl)
	
	inc_files = make_one_level(dot_file, fp.get_abs_name(), top_rel_path, all_info)
	while len(inc_files) > 0:
		abs_name = inc_files[0]
		del inc_files[0]
		inc_files += make_one_level(dot_file, abs_name, top_rel_path, all_info)
	
	dot_file.write("}" + nl)
	dot_file.close()
	
	os.system("dot " + join(dest_dir, my_rel_name_dot) + " -T png > " + join(dest_dir, my_rel_name_png))
	
