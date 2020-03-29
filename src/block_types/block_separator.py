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

import utils

"""
SEPARATOR COMMENT

This type of comment is simple: between '/*!' and '*/' write any
text without any leading keyword.

/*! Category 1 */
pred1(...):- ...
pred2(...):- ...
pred3(...):- ...
/*! Category 2 */
pred4(...):- ...
/*! Category 3 */
pred5(...):- ...
pred6(...):- ...
/*! Category 4 */
pred7(...):- ...
pred8(...):- ...
pred9(...):- ...
pred10(...):- ...
"""

class separator_block:
	
	def __init__(self, block, line):
		L = len(block)
		self._descr = block[4:(L-2)]
		self._descr = utils.line_cleanup(self._descr)
		
	def show(self, tab = ""):
		print("%sSeparator block" % tab)
		print("%s    Description: '%s'" % (tab, self._descr))
	
	def get_descr(self):
		return self._descr
