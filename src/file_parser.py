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
		self._name = filename
		
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
					self._load_predicates.append(line)
				else:
					file_inclusion = True
					current_line = line
				
			elif file_inclusion and dot != -1:
				file_inclusion = False
				current_line += line
				self._load_predicates.append(current_line)
			
			elif opens_sc != -1:
				# line opens a block comment
				if inside_sc:
					print utils.bc_in_bc
					exit(1)
				
				inside_sc = True
				current_line = line + " "
					
			elif closes_sc != -1:
				# line closes a block comment
				inside_sc = False
				current_line += " " + line
				self._doc_lines.append(current_line)
				
			elif inside_sc or file_inclusion:
				current_line += line + " "
			
			p += 1
		
		print "Parsed lines"
		for parsed in self._doc_lines:
			print "->", parsed
		
		print
		print "Lines with file inclusion"
		for load in self._load_predicates:
			print "->", load
	
	# Extract the predicate names, the format of the block documentation
	def extract_doc_info(self):
		for doc_line in self._doc_lines:
			B = block.doc_block(doc_line)
			self._blocks.append(B)
	
