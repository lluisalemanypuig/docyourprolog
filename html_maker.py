from os.path import abspath, relpath
import constants as csts
import file_parser
import utils
import formats

# write the head of the html file
class html_maker:
	file_descr = "<h1> Documentation for Prolog file: %s</h1>"
	
	# a predicate's label and its href in the same file
	preds_local_href = {}
	# a predicate's label and its global href: a hyperlink that
	# should open the html containing that predicate
	preds_global_href = {}
	
	# find all words starting with '@' and '?'.
	# Make sure those with '@' are a parameter, and display them appropriately
	# Make sure those with '?' are a predicates, and display them appropriately
	def _format_constr_descr(self, descr, param_names):
		form_param = formats.descr_parameter_format
		form_href_pred = formats.pred_local_cstr_format
		
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
				
				if label in html_maker.preds_global_href:
					href = html_maker.preds_local_href[label]
					print href
					words[i] = form_href_pred(label, href) + w[j:]
				
		return " ".join(words)
	
	def _write_head(self):
		nl = csts.nl
		HTML = self._html
		
		HTML.write("<head>" + nl)
		HTML.write("<title>" + self._short_name + "</title>" + nl)
		HTML.write("</head>" + nl)
	
	def _write_included_files_list(self):
		nl = csts.nl
		
		self._html.write("<a name=\"included_files\"></a>" + nl)
		self._html.write("<h2>Included files:</h2>" + nl)
		self._html.write("<ul id=\"included_files_list\">" + nl)
		
		for f in self._included_files:
			self._html.write(formats.included_file_format(f, f) + nl)
		self._html.write("</ul>" + nl)
	
	def _write_predicate_list(self):
		nl = csts.nl
		
		self._html.write("<a name=\"predicates\"></a>" + nl)
		self._html.write("<h2>Predicates:</h2>" + nl)
		self._html.write("<ul id=\"predicate_list\">" + nl)
		
		# iterate over all blocks
		for B in self._blocks:
			btype = B.block_type()
			binfo = B.block_info()
			if btype == "separator":
				if binfo.get_descr() != "":
					self._html.write( binfo.get_descr() + nl )
			elif btype == "predicate":
				label = binfo.get_predicate_label()
				href = html_maker.preds_local_href[label]
				self._html.write(formats.pred_list_format(label,href) + nl )
		
		self._html.write("</ul>" + nl)
	
	def _write_pred_form(self, binfo, name, all_param_names):
		form_param = formats.form_parameter_format
		
		nl = csts.nl
		self._html.write("<dt>" + nl)
		html_form = "<b>Form:</b> " + name + "("
		for i in range(0, len(all_param_names)):
			param_name = all_param_names[i]
			html_form += form_param(param_name)
			if i < len(all_param_names) - 1:
				html_form += ", "
		
		html_form += ")"
		self._html.write(html_form + nl)
		self._html.write("</dt>" + nl)
	
	def _write_pred_constrs(self, binfo, all_param_names, params):
		form_param = formats.cstr_parameter_format
		nl = csts.nl
		
		self._html.write("<dt>" + nl)
		constr_descr = "<b>Constraints: </b> "
		bcd = binfo.get_cstrs_descr()
		constr_descr += self._format_constr_descr(bcd, all_param_names)
		self._html.write(constr_descr + nl)
		
		# write parameter list
		self._html.write("<ul>" + nl)
		for pname in all_param_names:
			if pname in params:
				_, pdescr = params[pname]
				self._html.write("<li>" + nl)
				self._html.write(form_param(pname) + " ")
				pdescr = pdescr.split(' ')
				pdescr = " ".join(pdescr[1:])
				self._html.write(pdescr + nl)
				self._html.write("</li>" + nl)
			
		self._html.write("</ul>" + nl)
		self._html.write("</dt>" + nl)
	
	def _write_pred_descr(self, binfo, all_param_names):
		nl = csts.nl
		self._html.write("<dt>" + nl)
		pred_descr = "<b>Description: </b> "
		if binfo.get_description() != "":
			descr = binfo.get_description()
			pred_descr += self._format_constr_descr(descr, all_param_names)
		
		self._html.write(pred_descr + nl)
		self._html.write("</dt>" + nl)
	
	def _write_predicate_details(self):
		nl = csts.nl
		refmaker = lambda s: s.replace('/', '-')
		
		self._html.write("<a name=\"details\"></a>" + nl)
		self._html.write("<h2>Predicate Details:</h2>" + nl)
		self._html.write("<ul id=\"predicate_details\">" + nl)
		
		# iterate over all blocks
		for B in self._blocks:
			btype = B.block_type()
			binfo = B.block_info()
			if btype == "predicate":
				label = binfo.get_predicate_label()
				name = binfo.get_predicate_name()
				params = binfo.get_parameters()
				all_param_names = binfo.get_predicate_param_list()
				href = refmaker(label)
				
				self._html.write("<li>" + nl)
				self._html.write(formats.pred_title_format(label,href) + nl )
				self._html.write("<dl>" + nl)
				
				# write predicate form
				self._write_pred_form(binfo, name, all_param_names)
				
				# write predicate description
				self._write_pred_descr(binfo, all_param_names)
				
				# write predicate constraints
				if binfo.get_cstrs_descr() != "" or len(params) > 0:
					self._write_pred_constrs(binfo, all_param_names, params)
				
				self._html.write("</dl>" + nl)
				self._html.write("</li>" + nl)
		
		self._html.write("</ul>" + nl)
	
	def _write_body(self):
		nl = csts.nl
		HTML = self._html
		
		HTML.write("<body>" + nl)
		HTML.write((html_maker.file_descr % self._short_name) + nl)
		
		if "file" in self._class_blocks != None:
			file_descr = self._class_blocks["file"][-1]
			if file_descr.get_descr() != "":
				HTML.write("<p>" + file_descr.get_descr() + "</p>" + nl)
			if file_descr.get_author() != "":
				HTML.write("<p></b>    <i>" + file_descr.get_author() + "</i></p>" + nl)
			if file_descr.get_date() != "":
				HTML.write("<p><b>On</b>    <i>" + file_descr.get_date() + "</i></p>" + nl)
		
		if self._conf.FILE_INCLUSION_GRAPH and self._needs_graph:
			short_name, _ = utils.path_ext(self._short_name)
			HTML.write("<img src=\"" + short_name + ".png\" alt=\"file_inclusion_map\">" + nl)
		
		if len(self._included_files) > 0:
			self._write_included_files_list()
		
		if len(self._blocks) > 0:
			self._write_predicate_list()
			self._write_predicate_details()
		
		HTML.write(csts.html_git_footer)
		HTML.write("</body>" + nl)
	
	# fp: file parser object
	def __init__(self, conf, source_dir, all_info, fp):
		self._conf = conf
		
		self._abs_name = fp.get_abs_name()
		self._abs_path = fp.get_abs_path()
		self._rel_name = fp.get_rel_name()
		self._rel_path = fp.get_rel_path()
		self._short_name = fp.get_short_name()
		
		self._abs_html_name = fp.get_abs_html_name()
		self._abs_html_path = fp.get_abs_html_path()
		self._rel_html_name = fp.get_rel_html_name()
		self._rel_html_path = fp.get_rel_html_path()
		self._short_html_name = fp.get_short_html_name()
		
		self._included_files = []
		inc_files = fp.get_included_files()
		for i in range(0, len(inc_files)):
			their_rel_html_name = all_info[inc_files[i]].get_rel_html_name()
			html_name_href = relpath(their_rel_html_name, self._rel_html_path)
			self._included_files.append(html_name_href)
		
		self._needs_graph = fp.needs_inc_graph()
		self._blocks = fp.get_blocks()
		self._class_blocks = fp.get_class_blocks()
	
	def make_html_file(self):
		if self._abs_html_name == None:
			print "Internal error: absolute path to html file for '%s' was not set" % self._abs_name
			exit(1)
		
		self._html = utils.make_file(self._abs_html_name)
		
		self._html.write("<html>" + csts.nl)
		self._write_head()
		self._write_body()
		self._html.write("</html>" + csts.nl)
		
		self._html.close()

