"""
docyourprolog - Prolog parser for documentation generation
Copyright (C) 2018,2019,2020 Lluís Alemany Puig

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

from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
import utils
import block_types.block_doc as bdoc
import constants as csts
import constants.warnings_errors as WE
import constants.special as SC

"""
This class is used to parse the contents of a file: it is used to
extract the structured comments (or block comments) as defined in
block_types/ and to extract the file inclusion rules (or module
loading rules).
"""
class file_parser:
	# -----------------
	# STATIC ATTRIBUTES
	# -----------------
	
	# -------
	# METHODS
	# -------
	
	# *******
	# PRIVATE (do not call from outside)
	
	# Extract the necessary information from the file:
	# - the block comments
	# - the file inlcusion rules
	def _extract_information(self, filename):
		# read and store file
		f = open(filename, 'r')
		lines = []
		for line in f:
			lines.append(line)
		
		# extract information from file
		
		n_lines = len(lines)
		p = 0				# pointer to file line
		current_line = ""	# current line built
		ignore = 0			# ignore nested structured comments
		start_line = 0		# starting line of whatever is being parsed
		
		# state of parsing
		inside_sc = False		# parsing a structured comment
		file_inclusion = False	# parsing a file inclusion rule
		
		do_cleanup = True		# clean up the current line
		
		while p < n_lines:
			line = lines[p]
			# remove leading white spaces (spaces, tabs),
			# remove trailing white spaces (spaces, tabs, endlines),
			# remove anything after a '%'
			#
			# only when we are allowed to, or when the line has a
			# closing verbatim environment
			if do_cleanup or line.find(SC.close_verbatim) != -1:
				line = utils.string_cleanup(line)
			
			# ignore lines with only one comment (if a line contains
			# only a comment starting with '%' the result of its cleanup
			# is an empty string)
			if line == '' and lines[p].find('%'):
				pass
			
			if line == SC.open_verbatim:
				# if this line is an opening verbatim text, do not
				# make any cleanup on the line after reading it
				do_cleanup = False
			elif line == SC.close_verbatim:
				# if this line is a closing verbatim text, go back to
				# do cleanup on the line after reading it
				do_cleanup = True
			elif line == '':
				# empty lines within a structured comment are
				# interpreted as indications to make a new paragraph
				line = SC.new_line
			
			opens_sc = utils.opens_struct_comm(line)
			closes_sc = utils.closes_struct_comm(line)
			load = utils.loads_file(line)
			dot = line.find('.')
			
			if load:
				if dot != -1:
					self._load_predicates.append((p + 1,line))
				else:
					file_inclusion = True
					current_line = line
					start_line = p
				
			elif file_inclusion and dot != -1:
				file_inclusion = False
				current_line += line
				self._load_predicates.append((start_line + 1,current_line))
			
			elif opens_sc != -1:
				# line opens a block comment
				if inside_sc:
					ignore += 1
					WE.nested_block(p+1, ignore)
				else:
					inside_sc = True
					start_line = p
					
					# a block comment may be opened and
					# closed in the same line
					if closes_sc != -1:
						inside_sc = False
						self._doc_lines.append((p + 1,line))
					else:
						current_line = line + ' '
					
			elif closes_sc != -1:
				if ignore > 0:
					# discard ignored block comments
					ignore -= 1
				else:
					# line closes a block comment
					inside_sc = False
					current_line += ' ' + line
					self._doc_lines.append((start_line + 1,current_line))
				
			elif inside_sc or file_inclusion:
				current_line += line + ' '
			
			p += 1
	
	# Extract the information in each comment block
	# and the predicate's names
	def _extract_documentation(self):
		for doc_line in self._doc_lines:
			B = bdoc.doc_block(doc_line)
			self._blocks.append(B)
			btype = B.block_type()
			if btype == 'predicate':
				pred_block = B.block_info()
				self._pred_labels.append( pred_block.get_predicate_label() )
			
			if btype not in self._class_blocks:
				self._class_blocks[btype] = [B.block_info()]
			else:
				if btype == 'file':
					WE.multiple_file_descr()
				self._class_blocks[btype].append(B.block_info())
	
	# Extract the names of the files being included
	def _extract_included_files(self):
		
		for load in self._load_predicates:
			rule = load[1]
			inclusion = utils.inclusion_type(rule)
			
			if inclusion == 'ensure_loaded':
				name = utils.file_ensure_loaded(rule)
				self._included_files.append(name + '.pl')
			elif inclusion == '[':
				names = utils.files_brackets(rule)
				for name in names:
					self._included_files.append(name + '.pl')
			elif inclusion == 'use_module':
				name = utils.file_use_module(rule)
				if name != None:
					self._included_files.append(name + '.pl')
			else:
				WE.inclustion_type_unsupported(load)
	
	# ******
	# PUBLIC
	
	def __init__(self, source_dir, abs_name):
		# assuming that the source directory's absolute path
		# is '/home/user/dir1' we have that:
		# absolute: /home/user/dir1/dir2/file.pl
		# rel:      dir2/file.pl
		# short:    file.pl
		
		rel_name = relpath(abs_name, source_dir)
		abs_path, name_file = utils.abspath_name(abs_name)
		
		rel_name = utils.resolve_path(rel_name)
		abs_path = utils.resolve_path(abs_path)
		
		# absolute, rel and short name of the file to be parsed
		self._abs_name = abs_name
		self._abs_path = abs_path
		self._rel_name = rel_name
		self._rel_path = relpath(abs_path, source_dir)
		self._short_name = name_file
		
		self._abs_name = utils.resolve_path(self._abs_name)
		self._abs_path = utils.resolve_path(self._abs_path)
		self._rel_name = utils.resolve_path(self._rel_name)
		self._rel_path = utils.resolve_path(self._rel_path)
		
		self._abs_html_name = None		# to be set later
		self._abs_html_path = None		# to be set later
		self._rel_html_name = None		# """
		self._rel_html_path = None		# """
		self._short_html_name = None	# """
		
		self._rel_png_name = None		# """
		self._rel_png_path = None		# """
		self._rel_dot_name = None		# """
		self._rel_dot_path = None		# """
		
		# (T): temporary attribute
		self._doc_lines = []		# (T) all the lines with docs in the file
		self._load_predicates = []	# (T) lines with file inclusions
		
		self._blocks = []			# documentation blocks, stored in the
									# same order as they are parsed
		self._pred_labels = []		# names of the predicates
		self._included_files = []	# names of the included files
		self._class_blocks = {}		# blocks classified by type
	
	def parse_file(self):
		abs_path = self._abs_path
		abs_name = self._abs_name
		
		# check if file exists
		if not isfile(abs_name):
			WE.cant_read_file(abs_name)
			return
		
		self._extract_information(abs_name)
		self._extract_documentation()
		self._extract_included_files()
		
		for i in range(0, len(self._included_files)):
			f = self._included_files[i]
			a_path = join(abs_path, f)
			if a_path.find('..') != -1:
				a_path = utils.resolve_path(a_path)
			self._included_files[i] = a_path
		
		del self._doc_lines, self._load_predicates
	
	def set_rel_name(self, rel_name):
		self._rel_name = rel_name
	def set_short_name(self, short_name):
		self._short_name = short_name
	
	# :::::::
	# Getters
	
	def get_abs_name(self): return self._abs_name
	def get_abs_path(self): return self._abs_path
	def get_rel_name(self): return self._rel_name
	def get_rel_path(self): return self._rel_path
	def get_short_name(self): return self._short_name
	
	def get_abs_html_name(self): return self._abs_html_name
	def get_abs_html_path(self): return self._abs_html_path
	def get_rel_html_name(self): return self._rel_html_name
	def get_rel_html_path(self): return self._rel_html_path
	def get_short_html_name(self): return self._short_html_name
	
	def get_rel_png_name(self): return self._rel_png_name
	def get_rel_png_path(self): return self._rel_png_path
	def get_rel_dot_name(self): return self._rel_dot_name
	def get_rel_dot_path(self): return self._rel_dot_path
	
	def get_blocks(self): return self._blocks
	def get_class_blocks(self): return self._class_blocks
	def get_predicate_names(self): return self._pred_labels
	def get_included_files(self): return self._included_files
	
	def needs_inc_graph(self): return len(self._included_files) > 0
	
	def make_extra_names(self, dest_dir):
		if self._rel_name == None:
			WE.absolute_path_not_set(self._abs_name)
			exit(1)
		
		name_no_ext = splitext(self._short_name)[0]
		name_html = name_no_ext + '.html'
		
		self._abs_html_name = join(dest_dir, self._rel_path, name_html)
		self._abs_html_path = join(dest_dir, self._rel_path)
		self._rel_html_name = join(self._rel_path, name_html)
		self._rel_html_path = self._rel_path
		self._short_html_name = name_html
		
		name_png = name_no_ext + '.png'
		self._rel_png_name = join(self._rel_path, name_png)
		self._rel_png_path = self._rel_path
		
		name_dot = name_no_ext + '.dot'
		self._rel_dot_name = join(self._rel_path, name_dot)
		self._rel_dot_path = self._rel_path
		
		self._abs_html_name = utils.resolve_path(self._abs_html_name)
		self._abs_html_path = utils.resolve_path(self._abs_html_path)
		self._rel_html_name = utils.resolve_path(self._rel_html_name)
		self._rel_html_path = utils.resolve_path(self._rel_html_path)
		self._rel_png_name = utils.resolve_path(self._rel_png_name)
		self._rel_png_path = utils.resolve_path(self._rel_png_path)
		self._rel_dot_name = utils.resolve_path(self._rel_dot_name)
		self._rel_dot_path = utils.resolve_path(self._rel_dot_path)
		
