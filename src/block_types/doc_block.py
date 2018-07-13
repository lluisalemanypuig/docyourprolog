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
		self._type = None
		self._info = None
		
		lineno = line_block[0]
		block = line_block[1]
		
		firstw = block.split(' ')[0]
		
		if firstw.find("/*!") != -1:
			self._type = "separator"
			self._info = separator_block.separator_block(block, lineno)
		elif firstw.find("/***") != -1:
			self._type = "file"
			self._info = file_block.file_block(block, lineno)
		elif firstw.find("/**") != -1:
			self._type = "predicate"
			self._info = predicate_block.predicate_block(block, lineno)
		else:
			print "    Error: unrecognised block starting with '%s' at line %d" % (firstw, lineno)
	
	def block_type(self): return self._type
	def block_info(self): return self._info
	
		

