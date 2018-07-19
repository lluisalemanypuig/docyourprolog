# --------------------------------------------------------------------
# Platform-dependent 'constants' (values that are not meant to change)

import platform

nl = None
sep = None

# --------------------------------
# Platform-independent 'constants'

html_git_footer = None

# ----------------------------
# Method to make all constants

def make_constants():
	global nl, sep
	if platform.system() == "Linux":
		sep = "/"
		nl = "\n"
	elif platform.system() == "Windows":
		sep = "\\"
		nl = "\r\n"
	
	global html_git_footer
	html_git_footer = "<hr>"
	html_git_footer += "<p><a href=\""
	html_git_footer += "http://github.com/lluisalemanypuig/docyourprolog.git\">"
	html_git_footer += "Generated with DYP"
	html_git_footer += "</a></p>" + nl
