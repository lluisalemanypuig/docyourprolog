
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

# Returns true if the line tries to load a file
def loads_file(line):
	p = line.find(':-')
	while p > 0 and (line[p] == ' ' or line[p] == '\t'): p -= 1
	return p == 0

# Deletes all leading spaces and tabs.
# Deletes all characters after '%' and all preceding spaces and tabs
def delete_spaces_tabs(line):
	line_len = len(line)
	
	# delete leading spaces and tabs
	i = 0
	while i < line_len and (line[i] == ' ' or line[i] == '\t'):
		i += 1
	
	# find the last position of a code character
	j = line.find('%')
	while j > 0 and (line[j] == ' ' or line[j] == '\t'):
		j -= 1
	
	line = line[i:j]
	return line