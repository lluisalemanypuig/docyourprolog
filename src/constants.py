import platform

nl = None

def make_constants():
	global nl
	if platform.system() == "Linux":
		nl = "\n"
	elif platform.system() == "Windows":
		nl = "\r\n"
