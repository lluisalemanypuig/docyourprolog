
# Format a string 'label' as an element in the predicate list
# at the beginning of each file with a hyperlink 'href'.
def predicate_in_list(label, href):
	return "<li><p><a href=\"#%s\">%s</a></p></li>" % (href, label)
