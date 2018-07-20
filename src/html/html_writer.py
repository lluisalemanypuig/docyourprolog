import constants.platform_constants as pcsts
import constants.warnings_errors as WE
import utils

class html_writer:
	
	add_tab = set(['html', 'head', 'body', 'pre', 'ul', 'ol', 'li', 'dl'])
	
	def _put(self, content):
		envir = self._envir[-1]
		if envir in html_writer.add_tab:
			self._html.write(self._tab + content)
		else:
			self._html.write(content)
	
	def __init__(self, name):
		# name of the html file to create
		self._name = name
		
		# - what spacing de we have to add at the beginning
		#       when opening a new tab?
		# - which environment are we in?
		self._envir = []
		
		# tabulator for easy debugging of created html file
		self._tab = ''
		
		# add an endline after closing tag
		self._add_nl = []
	
	def __del__(self):
		is_closed = self.close()
		while not is_closed:
			is_closed = self.close()
	
	# Creates the html file and opens the environment '<html>'
	def start(self):
		self._html = utils.make_file(self._name)
		self._html.write(self._tab + '<html>' + pcsts.nl)
		self._envir.append('html')
		self._add_nl.append('html')
		self._tab += '\t'
	
	# Closes the last opened environment. Returns true if all
	# environments have been closed.
	def close(self):
		if len(self._envir) == 0:
			return True
		
		# environment to close
		envir = self._envir[-1]
		
		# write closing tag, properly indented
		if envir in html_writer.add_tab:
			# reduce by one the tabs
			self._tab = self._tab[:-1]
		
		# if current environment matches environment on top of 
		# stack then add an endline
		if envir == self._add_nl[-1]:
			self._put(('</%s>' % envir) + pcsts.nl)
			del self._add_nl[-1]
		else:
			self._put('</%s>' % envir)
		
		# delete closing tag
		del self._envir[-1]
		
		if len(self._envir) == 0:
			self._html.close()
			return True
		
		return False
	
	# Writes a string into the file
	def put(self, string):
		self._html.write(string)
	
	# Opens tag <head>
	def open_head(self):
		self._put('<head>' + pcsts.nl)
		self._envir.append('head')
		self._add_nl.append('head')
		self._tab += '\t'
	
	# Opens tag <body>
	def open_body(self):
		self._put('<body>' + pcsts.nl)
		self._envir.append('body')
		self._add_nl.append('body')
		self._tab += '\t'
	
	# Opens tag <title>
	def open_title(self):
		self._put('<title>')
		self._envir.append('title')
		self._add_nl.append('title')
	
	# Opens tag <p>
	def open_paragraph(self):
		self._put('<p>')
		self._envir.append('p')
		self._add_nl.append('p')
	
	# Opens tag <h1>
	def open_h1(self):
		self._put('<h1>')
		self._envir.append('h1')
		self._add_nl.append('h1')
	
	# Opens tag <h2>
	def open_h2(self):
		self._put('<h2>')
		self._envir.append('h2')
		self._add_nl.append('h2')
	
	# Opens tag <h3>
	def open_h3(self):
		self._put('<h3>')
		self._envir.append('h3')
		self._add_nl.append('h3')
	
	# Opens tag <pre>
	def open_verbatim(self):
		self._put('<pre>' + pcsts.nl)
		self._envir.append('pre')
		self._add_nl.append('pre')
		self._tab += '\t'
	
	# Opens tag <ul>
	# attrs is a dictionary. Keys supported
	# -> id
	def open_unordered_list(self, attrs = None):
		if attrs == None:
			self._put('<ul>' + pcsts.nl)
		else:
			# write attributes from attrs
			info = '<ul '
			if 'id' in attrs: info += 'id="' + attrs['id'] + '"'
			info += '>'
			self._put(info + pcsts.nl)
			
		self._envir.append('ul')
		self._add_nl.append('ul')
		self._tab += '\t'
	
	# Opens tag <ol>
	# attrs is a dictionary. Keys supported
	# -> id
	def open_ordered_list(self, attrs = None):
		if attrs == None:
			self._put('<ol>' + pcsts.nl)
		else:
			# write attributes from attrs
			info = '<ol '
			if 'id' in attrs: info += 'id="' + attrs['id'] + '"'
			info += '>'
			self._put(info + pcsts.nl)
			
		self._envir.append('ol')
		self._add_nl.append('ol')
		self._tab += '\t'
	
	# opens tag <dl>
	def open_description_list(self):
		self._put('<dl>' + pcsts.nl)
		self._envir.append('dl')
		self._add_nl.append('dl')
		self._tab += '\t'
	
	# to be used when in a description list
	# opens tag <dt>
	def define_term(self):
		self._put('<dt>')
		self._envir.append('dt')
		self._add_nl.append('dt')
	
	# to be used when in a description list
	# opens tag <dd>
	def describe_term(self):
		self._put('<dd>')
		self._envir.append('dd')
		self._add_nl.append('dd')
	
	# Opens tag <a>
	# attrs is a dictionary. Keys supported
	# -> name
	# -> href
	def open_a(self, attrs = None):
		if attrs == None:
			self._put('<a>')
		else:
			# write attributes from attrs
			info = '<a '
			if 'name' in attrs: info += 'name="' + attrs['name'] + '"'
			if 'href' in attrs: info += 'href="' + attrs['href'] + '"'
			info += '>'
			self._put(info)
			
		self._envir.append('a')
	
	# opens tag <li>
	def open_list_element(self):
		self._put('<li>' + pcsts.nl)
		self._envir.append('li')
		self._add_nl.append('li')
		self._tab += '\t'
	
	# opens tag <b>
	# attrs is a dictionary. Keys supported
	# -> style
	def open_bold(self, attrs = None):
		if attrs == None:
			self._put('<b>')
		else:
			info = '<b '
			if 'style' in attrs: info += 'style="' + attrs['style'] + '"'
			info += '>'
			self._put(info)
		
		self._envir.append('b')
	
	# opens tag <i>
	# attrs is a dictionary. Keys supported
	# -> style
	def open_italics(self, attrs = None):
		if attrs == None:
			self._put('<i>')
		else:
			info = '<i '
			if 'style' in attrs: info += 'style="' + attrs['style'] + '"'
			info += '>'
			self._put(info)
		
		self._envir.append('i')
		
		

