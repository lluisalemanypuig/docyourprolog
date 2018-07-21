
"""
Parameters in the description of a constrs environment, in the
form header, or the description of a predicate.
"""

# Returns html code to format a string found in a description
# which represents the name of a parameter.
def descr_parameter_format(param):
	return "<i style=\"color:#cc33ff\">%s</i>" % param

# Returns html code to format a string found in a predicate form
# which represents the name of a parameter.
def form_parameter_format(param):
	return "<i style=\"color:#ff0000\">%s</i>" % param

# Returns html code to format a string found at the beginning of a
# @param list (within the @cconstrs environment) which represents the
# name of a parameter.
def cstr_parameter_format(param):
	return "<i style=\"color:#0099ff\"><u>%s</u></i>" % param

"""
Labels of a predicate, in the predicate list, or in the description
of predicates or constraints.
"""

# Format a string 'label' when it is found in the description of
# a constraint or of a predicate as a hyperlink to 'href'. This
# label is a valid label of a predicate.
def pred_local_cstr_format(label, href):
	return "<a href=\"#%s\"><u>%s</u></a>" % (href, label)
def pred_global_cstr_format(label, href):
	return "<a href=\"%s\"><u>%s</u></a>" % (href, label)

# Format string 'label' as the title of a predicate description.
# This title appears in an itemised list. Its contents are Form,
# Description, ...
def pred_title_format(hw, label, name):
	hw.open_h3()
	hw.open_a({"name" : name})
	hw.put(label)
	hw.close_tag()
	hw.close_tag()
