import predicate_block
import file_block
import separator_block

class doc_block:
	
	def __init__(self, block):
		self._type = "which?"
		self._info = None
		
		print block
		
		p = block.find(' ')
		lead = block[0:p]
		if lead == "/*!":
			self._type = "separator"
			self._info = separator_block.separator_block(block)
		elif lead == "/**":
			self._type = "predicate"
			self._info = predicate_block.predicate_block(block)
		elif lead == "/***":
			self._type = "file"
			self._info = file_block.file_block(block)
		else:
			print "Unrecognized block comment"
			print block
	
	def block_type(self): return self._type
	def block_info(self): return self._info
		
		

