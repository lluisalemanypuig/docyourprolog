"""
docyourprolog - Prolog parser for documentation generation
Copyright (C) 2018 Lluís Alemany Puig

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact: Lluís Alemany Puig (lluis.alemany.puig@gmail.com)
"""

from os.path import join, relpath, isfile
import os

import file_parser
import constants.platform_constants as pcsts
import utils

def needs_run_dot(new_dot_string, dot_abs_name):
	if not isfile(dot_abs_name):
		return True
	
	old_dot_string = ''
	dot_file = open(dot_abs_name, 'r')
	for line in dot_file:
		old_dot_string += line
	
	if old_dot_string != new_dot_string:
		return True
	return False

def graph_to_png(graph, dot_abs_name, png_abs_name, conf):
	print "        + Construct graph"
	
	nl = pcsts.nl
	
	dot_string = ''
	dot_string += 'digraph file_graph {' + nl
	dot_string += 'node [shape=rectangle]' + nl
	dot_string += 'nodesep = 0.1' + nl
	dot_string += 'ranksep = 0.3' + nl
	
	for node,neighs in graph.iteritems():
		for n in neighs:
			dot_string += '"' + node + '" -> "' + n + '"' + nl
	
	dot_string += '}' + nl
	
	if needs_run_dot(dot_string, dot_abs_name):
		print "            - Running dot ..."
		
		dot_file = utils.make_file(dot_abs_name)
		dot_file.write(dot_string)
		dot_file.close()	
		
		os.system('dot ' + dot_abs_name + ' -T png > ' + png_abs_name)
		
		if not conf.CACHE_FILES:
			os.remove(dot_abs_name)
	else:
		print "            - No need to run dot"
		
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
			if f in dists:
				dists[f] = min(D + 1, dists[f])
			else:
				dists[f] = D + 1
			
			# if that distance is greater than the allowed,
			# do not add more vertices to graph
			if PGMD <= 0 or dists[f] <= PGMD:
			
				neigh_set.add( all_info[f].get_rel_name() )
				if f not in found_files:
					# this file has yet to be processed: add to 'queue'
					list_files.append(f)
					found_files.add(f)
		
		rel_name = all_info[abs_name].get_rel_name()
		if rel_name not in graph:
			graph[rel_name] = neigh_set
		else:
			graph[rel_name].update(neigh_set)
	
	dot_abs_name = join(dest_dir, '.cache', 'project_graph.dot')
	dot_abs_name = utils.resolve_path(dot_abs_name)
	
	png_abs_name = join(dest_dir, 'project_graph.png')
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
			if f in dists:
				dists[f] = min(D + 1, dists[f])
			else:
				dists[f] = D + 1
			
			# if that distance is greater than the allowed,
			# do not add more vertices to graph
			if FGMD <= 0 or dists[f] <= FGMD:
				
				neigh_set.add( all_info[f].get_rel_name() )
				if f not in found_files:
					# this file has yet to be processed: add to 'queue'
					list_files.append(f)
					found_files.add(f)
		
		rel_name = all_info[abs_name].get_rel_name()
		if rel_name not in graph:
			graph[rel_name] = neigh_set
		else:
			graph[rel_name].update(neigh_set)
	
	top_rel_path = fp.get_rel_path()
	my_short_name_pl = fp.get_short_name()
	my_rel_name_dot = fp.get_rel_dot_name()
	my_rel_name_png = fp.get_rel_png_name()
	
	dot_abs_name = join(dest_dir, '.cache', my_rel_name_dot)
	dot_abs_name = utils.resolve_path(dot_abs_name)
	
	png_abs_name = join(dest_dir, my_rel_name_png)
	png_abs_name = utils.resolve_path(png_abs_name)
	
	graph_to_png(graph, dot_abs_name, png_abs_name, conf)

