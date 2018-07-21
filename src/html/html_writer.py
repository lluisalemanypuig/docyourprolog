import constants.platform_constants as pcsts
import constants.warnings_errors as WE
import utils

class html_writer:
	
	def _full_tab(self): return "".join(self._ltab)
	def _tab(self): return "".join(self._ltab[:-1])
	
	def _open(self, tag):
		env = self._envir[-1]
		if env == self._tab_open[-1]: tag = self._tab() + tag
		if env == self._open_nl[-1]:  tag = tag + pcsts.nl
		self._html.write(tag)
	
	def _close(self, tag):
		env = self._envir[-1]
		if env == self._tab_close[-1]: tag = self._tab() + tag
		if env == self._close_nl[-1]:  tag = tag + pcsts.nl
		self._html.write(tag)
	
	def _single_line_env(self, env):
		self._envir.append(env)
		self._tab_open.append(env)
		self._open_nl.append('')
		self._tab_close.append('')
		self._close_nl.append(env)
		self._tab_cnt.append('')
		self._cnt_nl.append('')
		self._ltab.append('')
		
	def _multi_line_env(self, env):
		self._envir.append(env)
		self._tab_open.append(env)
		self._open_nl.append(env)
		self._tab_close.append(env)
		self._close_nl.append(env)
		self._tab_cnt.append(env)
		self._cnt_nl.append('')
		self._ltab.append('\t')
	
	def __init__(self, name):
		# name of the html file to create
		self._name = name
		
		# - what spacing de we have to add at the beginning
		#       when opening a new tab?
		# - which environment are we in?
		self._envir = []
		# environment list for which we have to add a/an
		self._tab_open = []		# tab before opening tag
		self._open_nl = []		# endline after opening tag
		self._tab_close = []	# tab before closing tag
		self._close_nl = []		# endline after closing tag
		self._tab_cnt = []		# tab before content
		self._cnt_nl = []		# endline after content
		# tabulator for indentation of html code
		self._ltab = []
		
	def __del__(self):
		is_open = (len(self._envir) > 0)
		while is_open:
			is_open = self.close_tag()
	
	# Closes the last opened environment. Returns true if all
	# environments have been close_tagd.
	def close_tag(self):
		if len(self._envir) == 0:
			return False
		
		# environment to close tag
		env = self._envir[-1]
		
		# close the environment
		self._close('</%s>' % env)
		
		# delete top of 'stack'
		del self._envir[-1]
		del self._tab_open[-1]
		del self._open_nl[-1]
		del self._tab_close[-1]
		del self._close_nl[-1]
		del self._tab_cnt[-1]
		del self._cnt_nl[-1]
		del self._ltab[-1]
		
		if len(self._envir) == 0:
			self._html.close()
			return False
		
		return True
	
	# Writes a string into the file
	def put(self, string):
		env = self._envir[-1]
		if env == self._tab_cnt[-1]: string = self._full_tab() + string
		if env == self._cnt_nl[-1]:  string = string + pcsts.nl
		self._html.write(string)
	
	# Creates the html file and opens the environment '<html>'
	def start(self):
		env = 'html'
		self._multi_line_env(env)
		self._html = utils.make_file(self._name)
		self._open('<%s>' % env)
		
	# Opens tag <head>
	def open_head(self):
		env = 'head'
		self._multi_line_env(env)
		self._open('<%s>' % env)
		
	# Opens tag <body>
	def open_body(self):
		env = 'body'
		self._multi_line_env(env)
		self._open('<%s>' % env)
		
	# Opens tag <title>
	def open_title(self):
		env = 'title'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# Opens tag <p>
	def open_paragraph(self):
		env = 'p'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# Opens tag <h1>
	def open_h1(self):
		env = 'h1'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# Opens tag <h2>
	def open_h2(self):
		env = 'h2'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# Opens tag <h3>
	def open_h3(self):
		env = 'h3'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# Opens tag <pre>
	def open_verbatim(self):
		env = 'pre'
		self._multi_line_env(env)
		self._open('<%s>' % env)
	
	def horizontal_line(self):
		self.put("<hr>" + pcsts.nl)
	
	# opens tag <dl>
	def open_description_list(self):
		env = 'dl'
		self._multi_line_env(env)
		self._open('<%s>' % env)
	
	# to be used when in a description list
	# opens tag <dt>
	def define_term(self):
		env = 'dt'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# to be used when in a description list
	# opens tag <dd>
	def describe_term(self):
		env = 'dd'
		self._single_line_env(env)
		self._open('<%s>' % env)
	
	# Adds an image to the source
	# attrs is a dictionary. Keys supported
	# -> name
	# -> alt
	def add_image(self, attrs):
		content = '<img'
		if "name" in attrs: content += ' src="' + attrs["name"] + '"'
		if "alt" in attrs: content += ' alt="' + attrs["alt"] + '"'
		content += '>'
		self.put(content)
	
	# Opens tag <ul>
	# attrs is a dictionary. Keys supported
	# -> id
	def open_unordered_list(self, attrs = None):
		env = 'ul'
		self._multi_line_env(env)
		
		if attrs == None:
			self._open('<%s>' % env)
		else:
			# write attributes from attrs
			info = '<%s ' % env
			if 'id' in attrs: info += 'id="' + attrs['id'] + '"'
			info += '>'
			self._open(info)
	
	# Opens tag <ol>
	# attrs is a dictionary. Keys supported
	# -> id
	def open_ordered_list(self, attrs = None):
		env = 'ol'
		self._multi_line_env(env)
		
		if attrs == None:
			self._open('<%s>' % env)
		else:
			# write attributes from attrs
			info = '<%s ' % env
			if 'id' in attrs: info += 'id="' + attrs['id'] + '"'
			info += '>'
			self._open(info)
	
	# Opens tag <a>
	# attrs is a dictionary. Keys supported
	# -> name
	# -> href
	def open_a(self, attrs = None):
		env = 'a'
		self._envir.append(env)
		self._tab_open.append('')
		self._open_nl.append('')
		self._tab_close.append('')
		self._close_nl.append('')
		self._tab_cnt.append('')
		self._cnt_nl.append('')
		self._ltab.append('')
		
		if attrs == None:
			self._open('<%s>' % env)
		else:
			# write attributes from attrs
			info = '<%s ' % env
			if 'name' in attrs: info += 'name="' + attrs['name'] + '"'
			if 'href' in attrs: info += 'href="' + attrs['href'] + '"'
			info += '>'
			self._open(info)
	
	# opens tag <li>
	def open_list_element(self):
		env = 'li'
		self._multi_line_env(env)
		self._open('<%s>' % env)
	
	# opens tag <b>
	# attrs is a dictionary. Keys supported
	# -> style
	def open_bold(self, attrs = None):
		env = 'b'
		self._envir.append(env)
		self._tab_open.append('')
		self._open_nl.append('')
		self._tab_close.append('')
		self._close_nl.append('')
		self._tab_cnt.append('')
		self._cnt_nl.append('')
		self._ltab.append('')
		
		if attrs == None:
			self._open('<%s>' % env)
		else:
			info = '<b '
			if 'style' in attrs: info += 'style="' + attrs['style'] + '"'
			info += '>'
			self._open(info)
	
	# opens tag <i>
	# attrs is a dictionary. Keys supported
	# -> style
	def open_italics(self, attrs = None):
		env = 'i'
		self._envir.append(env)
		self._tab_open.append('')
		self._open_nl.append('')
		self._tab_close.append('')
		self._close_nl.append('')
		self._tab_cnt.append('')
		self._cnt_nl.append('')
		self._ltab.append('')
		
		if attrs == None:
			self._open('<%s>' % env)
		else:
			info = '<b '
			if 'style' in attrs: info += 'style="' + attrs['style'] + '"'
			info += '>'
			self._open(info)
	
	# opens tag <u>
	# attrs is a dictionary. Keys supported
	# -> style
	def open_underlined(self, attrs = None):
		env = 'u'
		self._envir.append(env)
		self._tab_open.append('')
		self._open_nl.append('')
		self._tab_close.append('')
		self._close_nl.append('')
		self._tab_cnt.append('')
		self._cnt_nl.append('')
		self._ltab.append('')
		
		if attrs == None:
			self._open('<%s>' % env)
		else:
			info = '<b '
			if 'style' in attrs: info += 'style="' + attrs['style'] + '"'
			info += '>'
			self._open(info)
		
		

