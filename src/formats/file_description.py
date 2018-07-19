
# Title of a file
def file_title(filename):
	return "<h1> Documentation for Prolog file: %s</h1>" % filename

# Format a string that corresponds to the file description
def file_descr(descr):
	return "<p>%s</p" % descr

# Format a string that corresponds to the author of a file
def file_author(author):
	return "<p><b>By: </b><i>" + author + "</i></p>"

# Format a string that corresponds to the date of creation of a file
def file_date(date):
	return "<p><b>On: </b><i>" + date + "</i></p>"
