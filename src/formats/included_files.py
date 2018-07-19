
# Format string 'f' so that it opens the html file corresponding to
# the html documentation of the source file 'f'.pl
def included_file(f, href):
	return "<li><p><a href=\"%s\">%s</a></p></li>" % (href, f)
