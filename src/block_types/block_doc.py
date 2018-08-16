import constants.warnings_errors as WE
import block_predicate as bpred
import block_separator as bsep
import block_file as bfile

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
			self._info = bsep.separator_block(block, lineno)
		elif firstw.find("/***") != -1:
			self._type = "file"
			self._info = bfile.file_block(block, lineno)
		elif firstw.find("/**") != -1:
			self._type = "predicate"
			self._info = bpred.predicate_block(block, lineno)
		else:
			WE.unrecognised_block(firstw, lineno)
	
	def block_type(self):
		return self._type
	def block_info(self):
		return self._info
	
	

