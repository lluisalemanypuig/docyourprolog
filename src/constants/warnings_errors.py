import constants.special as SC

"""
Warnings
"""
def unrecognised_platform(plat):
	print "\tWarning: unrecognised platform '%s'." % plat
	print "\t\tAssuming Windows"

def nested_block(line, ignore):
	print "\tWarning (file_parser): Block comment within bigger block comment in line %d." % line
	print "\t\tIgnoring (%d) this block" % ignore

"""
Internal errors:
"""

def absolute_path_not_set(name):
	print "Internal error: absolute path to html file for '%s' was not set" % name

"""
External errors:
"""

def unmatched_tag_close_list():
	print "Error: unmatched tag '%s'" % SC.close_item_list
	print "    Did you leave blank lines between elements of the list?"

def item_not_within_list():
	print "Error: found an item tag but not within a list"
