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
		print "%sSeparator block" % tab
		print "%s    Description: '%s'" % (tab, self._descr)
