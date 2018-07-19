from os.path import join, relpath
import os

import file_parser
import constants.platform_constants as pcsts
import utils

def graph_to_png(graph, dot_abs_name, png_abs_name, conf):
	nl = pcsts.nl
	
	dot_file = utils.make_file(dot_abs_name)
	dot_file.write("digraph file_graph {" + nl)
	dot_file.write("node [shape=rectangle]" + nl)
	dot_file.write("nodesep = 0.1" + nl)
	dot_file.write("ranksep = 0.3" + nl)
	
	for node,neighs in graph.iteritems():
		for n in neighs:
			dot_file.write("\"" + node + "\" -> \"" + n + "\"" + nl)
	
	dot_file.write("}" + nl)
	dot_file.close()
	os.system("dot " + dot_abs_name + " -T png > " + png_abs_name)
	
	if not conf.KEEP_DOT:
		os.remove(dot_abs_name)

# makes the graph for all parsed files in all_info
def make_full_graph(dest_dir, all_info, conf):
	# -------------------------------------------------
	# Build the whole graph to find the source vertices
	
	# input degree of each node in the graph
	in_degree = {}
	# dictionary: {node : set of neighbours}
	graph = {}
	
	found_files = set([])
	list_files = []
	
	for abs_name in all_info:
		list_files.append(abs_name)
		in_degree[abs_name] = 0
	
	# build the graph while finding the sources
	while len(list_files) > 0:
		abs_name = list_files[0]
		del list_files[0]
		
		neigh_set = set([])
		inc_files = all_info[abs_name].get_included_files()
		for f in inc_files:
			in_degree[f] += 1
			neigh_set.add( all_info[f].get_rel_name() )
			if f not in found_files:
				# this file has yet to be processed: add to 'queue'
				list_files.append(f)
				found_files.add(f)
		
		rel_name = all_info[abs_name].get_rel_name()
		if rel_name not in graph: graph[rel_name] = neigh_set
		else: graph[rel_name].update(neigh_set)
	
	# ------------------------------------------
	# Build the graph again, but only with those
	# vertices within the maximum distance
	
	PGMD = conf.PROJECT_GRAPH_MAX_DIAMETER
	graph = {}
	list_files = []
	
	# initialise distances
	dists = {}
	for f,d in in_degree.iteritems():
		if d == 0:
			dists[f] = 0
			list_files.append(f)
	
	found_files = set([])
	while len(list_files) > 0:
		abs_name = list_files[0]
		del list_files[0]
		
		# distance from the source to this node
		D = dists[abs_name]
		
		neigh_set = set([])
		inc_files = all_info[abs_name].get_included_files()
		for f in inc_files:
			
			# distance from the source to a neighbour of node
			if f in dists: dists[f] = min(D + 1, dists[f])
			else: dists[f] = D + 1
			
			# if that distance is greater than the allowed,
			# do not add more vertices to graph
			if PGMD <= 0 or dists[f] <= PGMD:
			
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
	
	graph_to_png(graph, dot_abs_name, png_abs_name, conf)

# makes the graph for the parsed file 'fp'
def make_single_graph(dest_dir, fp, all_info, conf):
	FGMD = conf.FILE_GRAPH_MAX_DIAMETER
	# dictionary: {node : set of neighbours}
	graph = {}
	# distance from the source to the node
	dists = {fp.get_abs_name() : 0}
	
	found_files = set([])
	list_files = [fp.get_abs_name()]
	while len(list_files) > 0:
		abs_name = list_files[0]
		del list_files[0]
		
		# distance from the source to this node
		D = dists[abs_name]
		
		neigh_set = set([])
		inc_files = all_info[abs_name].get_included_files()
		for f in inc_files:
			
			# distance from the source to a neighbour of node
			if f in dists: dists[f] = min(D + 1, dists[f])
			else: dists[f] = D + 1
			
			# if that distance is greater than the allowed,
			# do not add more vertices to graph
			if FGMD <= 0 or dists[f] <= FGMD:
			
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
	
	graph_to_png(graph, dot_abs_name, png_abs_name, conf)
	
