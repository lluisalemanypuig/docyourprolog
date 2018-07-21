import predicate_details as PD
import constants.special as SC
import utils

"""
Format a space-separated list of strings with html code:
	-> Check that words starting with @ are parameters of predicates.
	   If so display them in italics and in purple.
	-> Check that words starting with ? are names of predicates in
	   the list param_names. If so, make them a hyperlink.

Returns a list of strings. Each string represents a paragraph.
"""
def colour_n_link_descr(descr, param_names, pred_names):
	form_param = PD.descr_parameter_format
	form_href_pred = PD.pred_local_cstr_format
	
	words = descr.split(' ')
	for i in range(0, len(words)):
		w = words[i]
		if w.find('@') != -1:
			j = len(w) - 1
			while j > 0 and not utils.is_alphanumeric(w[j]): j -= 1
			j += 1
			
			if w[1:j] in param_names:
				words[i] = form_param(w[1:j]) + w[j:]
		elif w.find('?') != -1:
			j = len(w) - 1
			while j > 0 and not utils.is_alphanumeric(w[j]): j -= 1
			j += 1
			
			label = w[1:j]
			
			if label in pred_names:
				href = label.replace('/', '-')
				words[i] = form_href_pred(label, href) + w[j:]
	
	return " ".join(words)

"""
Returns a list of strings. Each string is meant to start at a new line.
"""
def make_new_lines(descr):
	# find all special strings indicating 'new line' and split the string
	print descr
	descr = descr.split(SC.new_line)
	print descr
	return map(utils.line_cleanup, descr)
