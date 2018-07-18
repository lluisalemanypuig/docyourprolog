
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

def pred_ref_format(predlabel, href):
	return "<a href=\"#%s\"><u>%s</u></a>" % (href, predlabel)
