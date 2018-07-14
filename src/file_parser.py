from os.path import abspath, dirname, isfile
from os.path import join, splitext, relpath
import utils
import block_types.doc_block as dblock
import constants

class file_parser:
	# -----------------
	# STATIC ATTRIBUTES
	# -----------------
	
	# -------
	# METHODS
	# -------
	
	# *******
	# PRIVATE (do not call from outside)
	
	# Extract the documentation from the file, found in block comments
	def _extract_information(self, filename):
		# read and store file
		f = open(filename, 'r')
		lines = []
		for line in f: lines.append(line)
		
		# extract information from file
		
		# Extracts rules and structured comments.
		# The opening and closing of a structured must be the same. The
		# opening must begin with '/*' and the closing must end with '*/'.
		# Does not store lines with only a '%'-comment
		
		n_lines = len(lines)
		p = 0				# pointer to file line
		current_line = ""	# current line built
		inside_sc = False
		file_inclusion = False
		ignore = 0
		start_line = 0
		
		while p < n_lines:
			line = utils.string_cleanup(lines[p])
			
			# ignore lines with only one comment
			if line == '': pass
			
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
					print "Block comment within bigger block comment in line", p + 1
					print "    Ignoring (%d) this block" % ignore
				else:
					inside_sc = True
					start_line = p
					
					# a block comment may be opened and
					# closed in the same line
					if closes_sc != -1:
						inside_sc = False
						self._doc_lines.append((p + 1,line))
					else:
						current_line = line + " "
					
			elif closes_sc != -1:
				if ignore > 0:
					# discard ignored block comments
					ignore -= 1
				else:
					# line closes a block comment
					inside_sc = False
					current_line += " " + line
					self._doc_lines.append((start_line + 1,current_line))
				
			elif inside_sc or file_inclusion:
				current_line += line + " "
			
			p += 1
	
	# Extract the information in each comment block
	# and the predicate's names
	def _extract_documentation(self):
		for doc_line in self._doc_lines:
			B = dblock.doc_block(doc_line)
			self._blocks.append(B)
			if B.block_type() == "predicate":
				pred_block = B.block_info()
				self._pred_names.append( pred_block.get_predicate_name() )
	
	# Extract the names of the files being included
	def _extract_included_files(self):
		
		def inclusion_type(rule):
			i = rule.find(':')
			i += 2
			# place 'i' at the beginning of rule
			while i < len(rule) and utils.empty_space(rule[i]): i += 1
			# place 'j' at the end of rule
			j = i
			while j < len(rule) and rule[j] != '(' and rule[j] != '[': j += 1
			if i == j: return rule[i:(j+1)]
			return rule[i:j]
			
		for load in self._load_predicates:
			rule = load[1]
			inclusion = inclusion_type(rule)
			
			if inclusion == "ensure_loaded":
				name = utils.file_ensure_loaded(rule)
				self._included_files.append(name + ".pl")
			elif inclusion == "[":
				names = utils.files_brackets(rule)
				for name in names:
					self._included_files.append(name + ".pl")
			elif inclusion == "use_module":
				name = utils.file_use_module(rule)
				if name != None:
					self._included_files.append(name + ".pl")
			else:
				print "Error: unsupported inclusion type in line %d: '%s'" % load
	
	# ******
	# PUBLIC
	
	def __init__(self, filename):
		# assuming that the main directory's absolute path
		# specified in option -d, --main-dir is /home/user/dir1
		# we have that:
		
		# absolute: /home/user/dir1/dir2/file.pl
		# relative: dir2/file.pl
		# short:    file.pl
		
		# absolute, relative and short name of the file to be parsed
		self._abs_name = filename
		self._relative_name = None	# to be set later
		self._short_name = None		# """
		
		self._abs_html = None		# to be set later
		self._relative_html = None	# """
		self._short_html = None		# """
		
		# (T): temporary attribute
		self._doc_lines = []		# (T) all the lines with docs in the file
		self._load_predicates = []	# (T) lines with file inclusions
		
		self._blocks = []			# documentation blocks, parsed
		self._pred_names = []		# names of the predicates
		self._included_files = []	# names of the included files
		
		# check if file exists
		if not isfile(filename):
			print "    Error: could not read file '%s'" % filename
			return
		
		self._extract_information(filename)
		self._extract_documentation()
		self._extract_included_files()
		
		del self._doc_lines, self._load_predicates
	
	def set_relative_name(self, rel_name):
		self._relative_name = rel_name
	def set_short_name(self, short_name):
		self._short_name = short_name
	
	# :::::::
	# Getters
	
	def get_abs_name(self): return self._abs_name
	def get_relative_name(self): return self._relative_name
	def get_short_name(self): return self._short_name
	def get_abs_html(self): return self._abs_html
	def get_relative_html(self): return self._relative_html
	def get_short_html(self): return self._short_html
	
	def get_blocks(self): return self._blocks
	def get_predicate_names(self): return self._pred_names
	def get_included_files(self): return self._included_files
	
	def make_html_names(self, dest_dir):
		if self._relative_name == None:
			print "Internal error: relative name not set for file: '%s'" % self._abs_name
			return
		
		relative_path, name_pl = utils.path_name(self._relative_name)
		name_html = splitext(name_pl)[0] + ".html"
		
		self._abs_html = join(dest_dir, relative_path, name_html)
		self._relative_html = utils.path_ext(self._relative_name)[0] + ".html"
		self._short_html = name_html
		
	def make_html_file(self):
		if self._abs_html == None:
			print "Internal error: absoulte path to html file for '%s' was not set" % self._abs_name
			exit(1)
		
		html = utils.make_file(self._abs_html)
		html.write('Hey!')
		html.write('How are you?')
		html.close()
		
