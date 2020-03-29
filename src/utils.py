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

from os import listdir, makedirs
from os.path import exists, abspath, dirname, isfile
from os.path import join, splitext, relpath, split
import constants.platform_constants as pcsts

# Returns true if character is either a letter or a number
def is_alphanumeric(c):
	if 'a' <= c and c <= 'z':
		return True
	if 'A' <= c and c <= 'Z':
		return True
	if '0' <= c and c <= '9':
		return True
	return False

# Returns the position of the opening of the structured comment
def opens_struct_comm(line):
	return line.find('/*')

# Returns the position of the closing of the structured comment
def closes_struct_comm(line):
	return line.find('*/')

# Returns true if the character is an empty space (either a blank
# space, a tabulator or an endline character)
def empty_space(c):
	return c == ' ' or c == '\t' or c == pcsts.nl

# Returns true if the line tries to load a file
def loads_file(line):
	p = line.find(':-')
	while p > 0 and empty_space(line[p]):
		p -= 1
	return p == 0

# If a string finishes with '*/', delete it
# delete also leading and trailing empty characters
def line_cleanup(line):
	i = len(line) - 3
	if line.find('*/') == -1:
		i = len(line) - 1
	
	while i > 0 and empty_space(line[i]):
		i -= 1
	return line[0:(i+1)]

# Deletes all leading spaces and tabs.
def lstring_cleanup(line):
	line_len = len(line)
	
	# delete leading spaces and tabs
	i = 0
	while i < line_len and empty_space(line[i]):
		i += 1
	return line[i:]

# Deletes all characters after '%' and all trailing spaces and tabs
def rstring_cleanup(line):
	# find the last position of a code character
	j = line.find('%')
	if j != -1:
		while j > 0 and empty_space(line[j]):
			j -= 1
	else:
		if len(line) == 1:
			# sinle end-line character
			j = 1
		else:
			j = len(line) - 1
			while j > 0 and empty_space(line[j]):
				j -= 1
	return line[:(j+1)]

# left and right string cleanup
def string_cleanup(line):
	return lstring_cleanup( rstring_cleanup(line) )

# deletes simple quotes (') and double quotes (") from the name
def filename_cleanup(filename):
	filename = filename.replace("'", "")
	filename = filename.replace('"', "")
	return filename

# rule is of the form ':-ensure_loaded(file).'
# returns 'file'.
def file_ensure_loaded(rule):
	op = rule.find('(')
	cp = rule.find(')')
	filename = rule[(op+1):cp]
	return filename_cleanup(line_cleanup(filename))

# rule is of the form ':-[file1,file2,...,fileN]'
# returns all files between the brackets
def files_brackets(rule):
	ob = rule.find('[')
	cb = rule.find(']')
	return list(map(filename_cleanup, rule[(ob+1):cb].split(',')))

# rule is of the form ':-use_module(library(system))'
# returns all files between the brackets
def file_use_module(rule):
	if rule.find('library') != -1:
		# ignore library modules
		return None
	
	op = rule.find('(')
	cp = rule.find(')')
	comma = rule.find(',')
	if comma == -1:
		# parse use_module/1
		filename = rule[(op+1):cp]
		return filename_cleanup(filename)
	
	# parse use_module/2
	filename = rule[(op+1):comma]
	
	return filename_cleanup(filename)

# Given a string representing the inclusion of a file, return its
# type. For example:
# - for rule ':-[file1,file2].' returns '['
# - for rule ':-ensure_loaded(file).' returns 'ensure_loaded'
# - for rule ':-use_module(file).' returns 'use_module'
# - for rule ':-use_module(file, [pred1,pred2]).' returns 'use_module'
def inclusion_type(rule):
	i = rule.find(':')
	i += 2
	# place 'i' at the beginning of rule
	while i < len(rule) and empty_space(rule[i]):
		i += 1
	# place 'j' at the end of rule
	j = i
	while j < len(rule) and rule[j] != '(' and rule[j] != '[':
		j += 1
	if i == j:
		return rule[i:(j+1)]
	return rule[i:j]

# returns the file's path and name
def path_name(filename):
	return split(filename)

# splits the string into the extension and the rest
# given a string: 'asdf/qwer/zxcv.ext' returns
# ('asdf/qwer/zxcv', '.ext')
# given a string: 'zxcv.ext' returns
# ('zxcv', '.ext')
def path_ext(filename):
	return splitext(filename)

# returns the file's absolute path and the file's name
# given a string: 'asdf/qwer/zxcv.ext' returns
# ('/absolute/path/to/the/file/asdf/qwer', 'zxcv.ext')
def abspath_name(rel_path):
	abs_path = abspath(rel_path)
	dir_path = dirname(abs_path)
	name = relpath(rel_path, dir_path)
	return (dir_path, name)

# returns the file's full name
# given a string: 'asdf/qwer/zxcv.ext' returns
# '/absolute/path/to/the/file/zxcv.ext'
def absolute_filename(filename):
	path, name = abspath_name(filename)
	return join(path, name)

# Delete all those goddam '..' and '.' from an absolute path
def resolve_path(apath):
	# decide what separator
	sep = pcsts.sep
	
	while apath.find('..') != -1:
		partspath = apath.split(sep)
		i = partspath.index('..')
		if i == 0:
			print("Internal error: path '%s' has a '..' at the beginning" % apath)
			print("    Cannot resolve")
			exit(1)
		
		del partspath[i]
		del partspath[i - 1]
		apath = sep.join(partspath)
	
	while apath.find('.' + sep) != -1:
		partspath = apath.split(sep)
		i = partspath.index('.')
		del partspath[i]
		apath = sep.join(partspath)
	
	# if a '/.' is found at the end of the string
	if apath.find(sep + '.') == len(apath) - 1:
		apath = apath[0:-2]
	return apath

# opens the file in 'w+' mode and returns the object
# this works for relative and absolute paths
def make_file(abs_file_name):
	dir_path = dirname(abs_file_name)
	file_name = relpath(abs_file_name, dir_path)
	if dir_path != "" and not exists(dir_path):
		makedirs(dir_path)
	f = open(abs_file_name, "w+")
	return f
