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
	
	# ******
	# PUBLIC
	
	def __init__(self):
		self._name = "none"			# name of the file
		self._doc_lines = []		# all the lines with docs in the file
		self._load_predicates = []	# lines with file inclusions
		
		self._blocks = []			# documentation blocks, parsed
		self._pred_names = []		# names of the predicates
		self._included_files = []	# names of the included files
	
	# Extract the documentation from the file, found in block comments
	def extract_documentation(self, filename):
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
			line = utils.delete_spaces_tabs(lines[p])
			
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
		
		print "Parsed lines with documentation"
		for parsed in self._doc_lines:
			print "->", parsed
		
		print
		print "Lines with file inclusion"
		for load in self._load_predicates:
			print "=>", load
		
		print
	
	# Extract the predicate names, the format of the block documentation
	def extract_doc_info(self):
		for doc_line in self._doc_lines:
			B = block.doc_block(doc_line)
			self._blocks.append(B)
			if B.block_type() == "predicate":
				pred_block = B.block_info()
				self._pred_names.append( pred_block.get_predicate_name() )
		
		print "Predicate names in file '%s'" % self._filename
		print "    ", self._pred_names
