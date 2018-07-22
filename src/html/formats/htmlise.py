import constants.platform_constants as pcsts
import constants.warnings_errors as WE
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
	descr = descr.split(SC.new_line)
	return map(utils.line_cleanup, descr)

def make_item_list(HTML, itemlist):
	return None

"""
Makes environments: given a string of space-separated words with
special delimiters (opening and closing verbatim environments, itemised
lists, ...) writes in html format the corresponding environments.

hw: html_writer object
"""
def make_environments(HTML, descr):
	list_items = []
	it = 0
	
	while len(descr) > 0:
		it, token = get_next_token(descr, it)
		while it != -1 and token == 'cverb':
			it += SC.cverbl
			it, token = get_next_token(descr, it)
		
		# if nothing is found, it is a term
		if it != -1 and utils.string_cleanup(descr[0:it]) != '':
			HTML.define_term()
			HTML.put(descr[0:it])
			HTML.close_tag()
		
		# we found whatever token. anything in
		# descr[0:it] is simple text
		if it == -1:
			HTML.define_term()
			HTML.put(descr)
			HTML.close_tag()
			descr = ''
			pass
		
		if token == 'olist':
			HTML.open_unordered_list()
			descr = descr[(it + SC.olistl):]
			list_items.append(0)
			it = 0
			
		elif token == 'clist':
			if len(list_items) == 0:
				WE.unmatched_tag_close_list()
				exit(1)
			
			if list_items[-1] > 0:
				HTML.close_tag()
			
			HTML.close_tag()
			del list_items[-1]
			
			descr = descr[(it + SC.clistl):]
			it = 0
			
		elif token == 'overb':
			HTML.open_verbatim()
			
			# find the closing verbatim
			it2, token = get_next_token(descr, it)
			while token != 'cverb':
				it2 += SC.cverbl
				it2, token = get_next_token(descr, it2)
			
			# once found, put the contents in the html and close
			HTML.put(descr[(it + SC.overbl):it2])
			HTML.close_tag()
			
			descr = descr[(it2 + SC.cverbl):]
			it = 0
		
		elif token == 'item':
			if list_items[-1] > 0:
				HTML.close_tag()
			
			list_items[-1] += 1
			HTML.open_list_element()
			
			descr = descr[(it + SC.clistl):]
			
			# find next token: whatever is found in descr[0:w]
			# is text for the first item
			w,wt = get_next_token(descr,0)
			HTML.put(descr[0:w] + pcsts.nl)
			
			descr = descr[w:]
			it = 0
		
def get_next_token(descr, it):
	olist = descr.find(SC.open_item_list, it)
	clist = descr.find(SC.close_item_list, it)
	overb = descr.find(SC.open_verbatim, it)
	cverb = descr.find(SC.close_verbatim, it)
	item = descr.find(SC.item_list, it)
	
	values = [
		(olist, 'olist'), (clist, 'clist'),
		(overb, 'overb'), (cverb, 'cverb'),
		(item, 'item')
	]
	values = filter(lambda (p,t): p != -1, values)
	if len(values) == 0: return (-1,None)
	
	values = sorted(values)
	return values[0]
	
		
	
