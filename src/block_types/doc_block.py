import predicate_block
import file_block
import separator_block

class doc_block:
	
	doc_block_types = {
		"separator" : "/*!",
		"predicate" : "/**",
		"file" : "/***"
	}
	
	def __init__(self, line_block):
		self._type = "which?"
		self._info = None
		
		line = line_block[0]
		block = line_block[1]
		
		if block.find("/*!") != -1:
			self._type = "separator"
			print "Separator:"
			self._info = separator_block.separator_block(block, line)
		elif block.find("/***") != -1:
			self._type = "file"
			print "File:"
			self._info = file_block.file_block(block, line)
		elif block.find("/**") != -1:
			self._type = "predicate"
			print "Predicate:"
			self._info = predicate_block.predicate_block(block, line)
		else:
			print "Unrecognized block comment: '%s'" % block
	
	def block_type(self): return self._type
	def block_info(self): return self._info
		
		

