import utils
import block_types.doc_block as block

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
		self._filename = filename
		
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
	
	# Extract the predicate names
	def _extract_documentation(self):
		for doc_line in self._doc_lines:
			B = block.doc_block(doc_line)
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
				self._included_files.append(name)
			elif inclusion == "[":
				names = utils.files_brackets(rule)
				for name in names[0]:
					self._included_files.append((name,None))
			elif inclusion == "use_module":
				names = utils.file_use_module(rule)
				if names != None: self._included_files.append(names)
			else:
				print "Error: unsupported inclusion type in line %d: '%s'" % load
	
	# ******
	# PUBLIC
	
	def __init__(self, filename, pred_filt):
		self._filename = filename	# name of the file
		
		# (T): temporary attribute
		self._doc_lines = []		# (T) all the lines with docs in the file
		self._load_predicates = []	# (T) lines with file inclusions
		
		self._blocks = []			# documentation blocks, parsed
		self._pred_names = []		# names of the predicates
		self._included_files = []	# names of the included files
		
		self._extract_information(filename)
		
		print "+++ Parsed lines with documentation"
		for parsed in self._doc_lines: print "->", parsed
		print
		print "+++ Lines with file inclusion"
		for load in self._load_predicates: print "=>", load
		print
		
		self._extract_documentation()
		print
		
		# filter predicate blocks: delete those corresponding to
		# the predicates that are NOT in pred_filt
		for B in self._blocks:
			if B.block_type() == "predicate":
				bname = B.block_info().get_predicate_name()
				if bname not in pred_filt:
					self._blocks.remove(B)
					self._pred_names.remove(bname)
		
		self._extract_included_files()
		
		print "+++ Filtered block comments"
		for B in self._blocks:
			if B.block_info() == "None":
				print "Null block info"
			B.block_info().show()
		print "All methods to be shown:", self._pred_names
		print
		
		print "+++ Included files and predicates"
		for f in self._included_files:
			print "    ", f
		print
		
	def get_filename(self): self._filename
	def get_blocks(self): self._blocks
	def get_predicate_names(self): self._pred_names
	def get_included_files(self): self._included_files
