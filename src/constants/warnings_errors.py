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

import constants.special as SC

"""
Warnings
"""
def unrecognised_platform(plat):
	print("        Warning: unrecognised platform '%s'." % plat)
	print("            Assuming Windows")

def nested_block(line, ignore):
	print("        Warning (file_parser): Block comment within bigger block comment in line %d." % line)
	print("            Ignoring (%d) this block" % ignore)

def inclustion_type_unsupported(load):
	print("        Warning: unsupported inclusion type in line %d: '%s'" % load)

def multiple_file_descr():
	print("        Warning: more than one file description")

def unrecognised_block(firstw, lineno):
	print("        Warning: unrecognised block starting with '%s' at line %d" % (firstw, lineno))

"""
Internal errors:
"""

def absolute_path_not_set(name):
	print("        Internal error: absolute path to html file for '%s' was not set" % name)

def wrong_environment():
	print("        Internal error: wrong environment", environment)

def too_many_param_defs(pname, line):
	print("        Error: at least two @param defining '%s'" % pname)
	print("            In block comment starting at line", line)

def too_many_param(line):
	print("        Warning: too many @param in @constrs environment in block")
	print("            starting at line %d" % line)

"""
External errors:
"""

def unmatched_tag_close_list():
	print("        Error: unmatched tag '%s'" % SC.close_item_list)
	print("            Did you leave blank lines between elements of the list?")

def item_not_within_list():
	print("        Error: found an item tag but not within a list")

def cant_read_file(filename):
	print("        Error: could not read file '%s'" % filename)
