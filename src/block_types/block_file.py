import utils

"""
http://prologdoc.sourceforge.net/


GENERAL FILE DOCUMENTATION
/***
	@descr This file is used for many things. Among them are:
		<ul>
		  <li> Purpose 1 blah blah blah
		  <li> Purpose 2 blah blah blah
		</ul>
	@author John Smith
	@date 1/1/00
*/
"""

class file_block:
	
	def _add_info(self, environment, info):
		if environment == "descr": self._descr = info[7:len(info)]
		elif environment == "author": self._author = info[8:len(info)]
		elif environment == "date": self._date = info[6:len(info)]
		else:
			# this should not happen
			print "Internal error: wrong environment", environment
	
	def __init__(self, block, line):
		self._descr = None
		self._author = None
		self._date = None
		
		descr = (block.find('@descr'), 'descr')
		author = (block.find('@author'), 'author')
		date = (block.find('@date'), 'date')
		
		info = sorted([descr, author, date])
		
		for i in range(0, len(info)):
			M = -1
			if i == len(info) - 1: M = len(block)
			else: M = info[i + 1][0] - 1
			
			content = block[info[i][0] : M]
			self._add_info(info[i][1], content)
		
		if self._descr != None:
			self._descr = utils.line_cleanup(self._descr)
		if self._author != None:
			self._author = utils.line_cleanup(self._author)
		if self._date != None:
			self._date = utils.line_cleanup(self._date)
	
	def show(self, tab = ""):
		print "%sFile block" % tab
		print "%s    File description: '%s' " % (tab, self._descr)
		print "%s    File author: '%s'" % (tab, self._author)
		print "%s    File date: '%s'" % (tab, self._date)
	
	def get_descr(self): return self._descr
	def get_author(self): return self._author
	def get_date(self): return self._date
