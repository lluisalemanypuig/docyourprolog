
# ----------------
# Verbose messages
# ----------------

# bc: block comment

bc_in_bc = "Who on Earth puts a block comment within a bigger block comment?!?!?\n\
    Please... fix it."

# ------------------
# Dealing with lines
# ------------------

# Returns the position of the opening of the structured comment
def opens_struct_comm(line):
	return line.find('/*')

# Returns the position of the closing of the structured comment
def closes_struct_comm(line):
	return line.find('*/')

# Returns true if the character is an empty space (either a blank
# space, a tabulator or an endline character)
def empty_space(c):
	return c == ' ' or c == '\t' or c == '\n'

# Returns true if the line tries to load a file
def loads_file(line):
	p = line.find(':-')
	while p > 0 and empty_space(line[p]): p -= 1
	return p == 0

# If a string finishes with '*/', delete it
# delete also leading and trailing empty characters
def line_cleanup(line):
	i = len(line) - 3
	if line.find('*/') == -1: i = len(line) - 1
	
	while i > 0 and empty_space(line[i]): i -= 1
	return line[0:(i+1)]

# Deletes all leading spaces and tabs.
# Deletes all characters after '%' and all preceding spaces and tabs
def string_cleanup(line):
	line_len = len(line)
	
	# delete leading spaces and tabs
	i = 0
	while i < line_len and empty_space(line[i]): i += 1
	
	# find the last position of a code character
	j = line.find('%')
	if j != -1:
		while j > 0 and empty_space(line[j]): j -= 1
	else:
		if len(line) == 1:
			# sinle end-line character
			j = 1
		else:
			j = len(line) - 1
			while j > 0 and empty_space(line[j]): j -= 1
	
	line = line[i:(j+1)]
	return line

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
	return map(filename_cleanup, rule[(ob+1):cb].split(','))

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
	
