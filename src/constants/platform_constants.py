# --------------------------------------------------------------------
# Platform-dependent 'constants' (values that are not meant to change)

import platform
import warnings_errors as WE

nl = None	# endline character(s)
sep = None	# path-separator character:
			# C:\a\path\in\Windows
			# /a/path/in/Linux

# ----------------------------
# Method to make all constants

def make_constants():
	global nl, sep
	
	P = platform.system()
	if P == "Linux":
		sep = "/"
		nl = "\n"
	elif P == "Windows":
		sep = "\\"
		nl = "\r\n"
	else:
		WE.unrecognised_platform(P)
		sep = "\\"
		nl = "\r\n"

