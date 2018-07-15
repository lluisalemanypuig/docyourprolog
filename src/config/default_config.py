
"""
Where to find the source files.
"""
SRC_DIR					= None

"""
Where to store the documentation files.
"""
DEST_DIR				= None

"""
For every file, make a directed graph showing what files
include (load) what files. In this graph a directed
edge (A,B) means 'file A includes (loads) file B'.
"""
FILE_INCLUSION_GRAPH	= True

"""
Same as for FILE_INCLUSION_GRAPH but this graph contains
the graph for all the source files.
"""
PROJ_INCLUSION_GRAPH	= True

"""
Document all files found in the source directories
and the directories within it.
"""
RECURSIVE				= False

"""
Document all files whose extension match the ones
in the list.
"""
EXTENSIONS				= [".pl", ".prolog"]

"""
Document files included (loaded) by other files even
if they are in a folder different from the SRC_DIR and
the RECURSIVE variable is set to False.
"""
FOLLOW_INCLUDES			= True

