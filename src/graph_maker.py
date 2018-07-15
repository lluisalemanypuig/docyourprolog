from os.path import join, relpath
import os

import file_parser
import constants
import utils

def graph_to_png(graph, dot_abs_name, png_abs_name):
	nl = constants.nl
	
	dot_file = utils.make_file(dot_abs_name)
	dot_file.write("digraph file_graph {" + nl)
	
	for node,neighs in graph.iteritems():
		dot_file.write("\"" + node + "\" [shape=rectangle]" + nl)
		for n in neighs:
			dot_file.write("\"" + node + "\" -> \"" + n + "\"" + nl)
	
	dot_file.write("}" + nl)
	dot_file.close()
	os.system("dot " + dot_abs_name + " -T png > " + png_abs_name)

# makes the graph for all parsed files in all_info
def make_full_graph(dest_dir, all_info):
	
	# dictionary: {node : set of neighbours}
	graph = {}
	
	found_files = set([])
	list_files = [abs_name for abs_name in all_info.keys()]
	while len(list_files) > 0:
		abs_name = list_files[0]
		del list_files[0]
		
		neigh_set = set([])
		inc_files = all_info[abs_name].get_included_files()
		for f in inc_files:
			neigh_set.add( all_info[f].get_rel_name() )
			
			if f not in found_files:
				# this file has yet to be processed: add to 'queue'
				list_files.append(f)
				found_files.add(f)
		
		rel_name = all_info[abs_name].get_rel_name()
		if rel_name not in graph: graph[rel_name] = neigh_set
		else: graph[rel_name].update(neigh_set)
	
	dot_abs_name = join(dest_dir, "project_graph.dot")
	dot_abs_name = utils.resolve_path(dot_abs_name)
	
	png_abs_name = join(dest_dir, "project_graph.png")
	png_abs_name = utils.resolve_path(png_abs_name)
	
	print "    >> Make graph file"
	graph_to_png(graph, dot_abs_name, png_abs_name)

# makes the graph for the parsed file 'fp'
def make_single_graph(dest_dir, fp, all_info):
	
	# dictionary: {node : set of neighbours}
	graph = {}
	
	found_files = set([])
	list_files = [fp.get_abs_name()]
	while len(list_files) > 0:
		abs_name = list_files[0]
		del list_files[0]
		
		neigh_set = set([])
		inc_files = all_info[abs_name].get_included_files()
		for f in inc_files:
			neigh_set.add( all_info[f].get_rel_name() )
			
			if f not in found_files:
				# this file has yet to be processed: add to 'queue'
				list_files.append(f)
				found_files.add(f)
		
		rel_name = all_info[abs_name].get_rel_name()
		if rel_name not in graph: graph[rel_name] = neigh_set
		else: graph[rel_name].update(neigh_set)
	
	top_rel_path = fp.get_rel_path()
	my_short_name_pl = fp.get_short_name()
	my_rel_name_dot = fp.get_rel_dot_name()
	my_rel_name_png = fp.get_rel_png_name()
	
	dot_abs_name = join(dest_dir, my_rel_name_dot)
	dot_abs_name = utils.resolve_path(dot_abs_name)
	
	png_abs_name = join(dest_dir, my_rel_name_png)
	png_abs_name = utils.resolve_path(png_abs_name)
	
	print "    >> Make graph file"
	graph_to_png(graph, dot_abs_name, png_abs_name)
	
