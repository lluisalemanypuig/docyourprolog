"""
docyourprolog - Prolog parser for documentation generation
Copyright (C) 2018,2019,2020 Lluís Alemany Puig

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact: Lluís Alemany Puig (lluis.alemany.puig@gmail.com)
"""

import constants.platform_constants as pcsts
import constants.warnings_errors as WE
import html.formats.predicate_details as PD
import constants.special as SC
import utils

# colours a word containing parameter names
def colourise_word(w, param_names):
	form_param = PD.descr_parameter_format
	
	i = w.find('@')
	while i != -1:
		j = i + 1
		while j < len(w) and utils.is_alphanumeric(w[j]):
			j += 1
		
		param = w[(i+1):j]
		if param in param_names:
			w = w[0:i] + form_param(param) + w[j:]
		
		i = w.find('@', j)
	
	return w

"""
Format a space-separated list of strings with html code:
	-> Check that words starting with @ are parameters of predicates.
	   If so display them in italics and in purple.
	-> Check that words starting with ? are names of predicates in
	   the list param_names. If so, make them a hyperlink.

Returns a list of strings. Each string represents a paragraph.
"""
def colour_n_link_descr(descr, param_names, pred_names):
	form_href_pred = PD.pred_local_cstr_format
	
	words = descr.split(' ')
	for i in range(0, len(words)):
		w = words[i]
		if w.find('@') != -1:
			words[i] = colourise_word(words[i], param_names)
			
		elif w.find('?') != -1:
			j = len(w) - 1
			while j > 0 and not utils.is_alphanumeric(w[j]):
				j -= 1
			j += 1
			
			label = w[1:j]
			
			if label in pred_names:
				href = label.replace('/', '-')
				words[i] = form_href_pred(label, href) + w[j:]
	
	return " ".join(words)

"""
Makes environments: given a string of space-separated words with
special delimiters (opening and closing verbatim environments, itemised
lists, ...) writes in html format the corresponding environments.

hw: html_writer object
"""
def make_environments(HTML, descr):
	list_items = []
	prev_blanks = 0
	it = 0
	
	while len(descr) > 0:
		it, token = get_next_token(descr, it)
		while it != -1 and token == 'cverb':
			it += SC.cverbl
			it, token = get_next_token(descr, it)
		
		# if nothing is found, it is a term
		if it == -1:
			if prev_blanks >= 2:
				HTML.blank_line()
			HTML.define_term()
			HTML.put(descr)
			HTML.close_tag()
			descr = ''
			pass
		
		if token == 'blank':
			text = utils.string_cleanup(descr[0:it])
			if text != '':
				if prev_blanks >= 2:
					HTML.blank_line()
				HTML.define_term()
				HTML.put(text)
				HTML.close_tag()
			
			nblanks, next_text = peek_nblanks(descr, it)
			descr = descr[next_text:]
			it = 0
			
			prev_blanks = nblanks
		else:
			# we found whatever token. Anything 
			# in descr[0:it] is simple text
			if utils.string_cleanup(descr[0:it]) != '':
				if prev_blanks >= 2:
					HTML.blank_line()
					prev_blanks = 0
				HTML.define_term()
				HTML.put(descr[0:it])
				HTML.close_tag()
			
			if token == 'olist':
				if prev_blanks >= 2:
					HTML.blank_line()
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
				# find the closing verbatim
				it2, token = get_next_token(descr, it)
				while token != 'cverb':
					it2 += SC.cverbl
					it2, token = get_next_token(descr, it2)
				
				# once found, put the contents in the html and close
				verbtext = descr[(it + SC.overbl):it2]
				verbtext = utils.rstring_cleanup(verbtext)
				if verbtext != '':
					HTML.open_verbatim()
					HTML.put(verbtext + pcsts.nl)
					HTML.close_tag()
				
				descr = descr[(it2 + SC.cverbl):]
				it = 0
			
			elif token == 'item':
				if len(list_items) == 0:
					print(descr)
					WE.item_not_within_list()
					exit(1)
				
				if list_items[-1] > 0:
					HTML.close_tag()
				
				list_items[-1] += 1
				
				if prev_blanks >= 1:
					HTML.blank_line()
				HTML.open_list_element()
				
				descr = descr[(it + SC.clistl):]
				
				# find next token: whatever is found in descr[0:w]
				# is text for the first item
				w,wt = get_next_token(descr,0)
				
				HTML.define_term()
				HTML.put(descr[0:w])
				HTML.close_tag()
				
				descr = descr[w:]
				it = 0
			
			prev_blanks = 0

def get_next_token(descr, it):
	olist = descr.find(SC.open_item_list, it)
	clist = descr.find(SC.close_item_list, it)
	overb = descr.find(SC.open_verbatim, it)
	cverb = descr.find(SC.close_verbatim, it)
	blank = descr.find(SC.new_line, it)
	item = descr.find(SC.item_list, it)
	
	values = [
		(olist, 'olist'), (clist, 'clist'),
		(overb, 'overb'), (cverb, 'cverb'),
		(item, 'item'), (blank, 'blank')
	]
	values = list(filter(lambda p: p[0] != -1, values))
	if len(values) == 0:
		return (-1,None)
	
	values = sorted(values)
	return values[0]

# how many blanks IMMEDIATELY after 'at'
def peek_nblanks(descr, at):
	cnt = 1
	last_at = -1
	
	p = descr.find(SC.new_line, at + 1)
	while p != -1 and p == cnt*(SC.newlinel + 1) + at:
		cnt += 1
		last_at = p
		p = descr.find(SC.new_line, p + 1)
	
	if last_at != -1:
		last_at += (SC.newlinel + 1)
	else:
		last_at = at + (SC.newlinel + 1)
	
	return cnt, last_at
