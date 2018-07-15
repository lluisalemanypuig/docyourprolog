import platform

nl = None
sep = None

def make_constants():
	global nl
	if platform.system() == "Linux":
		sep = "/"
		nl = "\n"
	elif platform.system() == "Windows":
		sep = "\\"
		nl = "\r\n"
