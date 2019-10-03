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
	
	

