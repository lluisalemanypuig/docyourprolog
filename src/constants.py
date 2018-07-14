import platform

nl = None

def make_constants():
	global nl
	if platform.system() == "Linux":
		print "Working on Linux"
		nl = "\n"
	elif platform.system() == "Windows":
		print "Working on Windows"
		nl = "\r\n"
