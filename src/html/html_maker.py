from os.path import abspath, relpath

import file_parser
from html_writer import html_writer as hwriter
import utils

import constants.platform_constants as pcsts
import constants.warnings_errors as WE

import formats.file_description as FD
import formats.included_files as IF
import formats.predicate_list as PL
import formats.predicate_details as PD
import formats.htmlise as HS

# write the head of the html file
class html_maker:
	
	def _write_description(self, descr, all_param_names = []):
		HTML = self._hw
		descr = HS.colour_n_link_descr(descr, all_param_names, self._pred_names)
		
		HTML.open_description_list()
		HS.make_environments(HTML, descr)
		HTML.close_tag()
	
	def _write_head(self):
		self._hw.open_head()
		self._hw.put_meta({'charset' : 'UTF-8'})
		self._hw.open_title();
		self._hw.put(self._short_name);
		self._hw.close_tag()
		self._hw.close_tag()
	
	def _write_included_files_list(self):
		nl = pcsts.nl
		HTML = self._hw
		
		HTML.open_h2()
		HTML.open_a({'name' : 'included_files'})
		HTML.put('Included files:')
		HTML.close_tag()
		HTML.close_tag()
		HTML.open_unordered_list({'id' : 'included_files_list'})
		
		for f in self._included_files:
			IF.included_file(HTML, f, f)
			
		HTML.close_tag()
	
	def _write_predicate_list(self):
		nl = pcsts.nl
		HTML = self._hw
		
		HTML.open_h2()
		HTML.open_a({'name' : 'predicates'})
		HTML.put('Predicates:')
		HTML.close_tag()
		HTML.close_tag()
		HTML.open_unordered_list({'id' : 'predicate_list'})
		
		# iterate over all blocks
		for B in self._blocks:
			btype = B.block_type()
			binfo = B.block_info()
			if btype == 'separator':
				if binfo.get_descr() != '':
					descr = binfo.get_descr()
					self._write_description(descr, [])
					
			elif btype == 'predicate':
				label = binfo.get_predicate_label()
				href = label.replace('/','-')
				PL.predicate_in_list(HTML, label,href)
		
		HTML.close_tag()
	
	def _write_pred_form(self, binfo, name, all_param_names):
		form_param = PD.form_parameter_format
		nl = pcsts.nl
		HTML = self._hw
		
		HTML.define_term()
		HTML.open_bold()
		HTML.put('Form: ')
		HTML.close_tag()
		HTML.close_tag()
		
		HTML.describe_term()
		
		html_form = name + '('
		for i in range(0, len(all_param_names)):
			param_name = all_param_names[i]
			html_form += form_param(param_name)
			if i < len(all_param_names) - 1:
				html_form += ', '
		
		html_form += ')'
		HTML.put(html_form)
		HTML.close_tag()
	
	def _write_pred_descr(self, binfo, all_param_names):
		nl = pcsts.nl
		HTML = self._hw
		
		HTML.define_term()
		HTML.open_bold()
		HTML.put('Description:')
		HTML.close_tag()
		HTML.close_tag()
		
		if binfo.get_description() != '':
			descr = binfo.get_description()
			self._write_description(descr, all_param_names)
	
	def _write_pred_constrs(self, binfo, all_param_names, params):
		form_param = PD.cstr_parameter_format
		nl = pcsts.nl
		HTML = self._hw
		
		HTML.define_term()
		HTML.open_bold()
		HTML.put('Constraints:')
		HTML.close_tag()
		HTML.close_tag()
		
		bcd = binfo.get_cstrs_descr()
		self._write_description(bcd, all_param_names)
		
		# write parameter list
		HTML.open_unordered_list()
		for pname in all_param_names:
			if pname in params:
				_, pdescr = params[pname]
				
				HTML.open_list_element()
				pnamelist = form_param(pname) + ' '
				pdescr = pdescr.split(' ')
				pdescr = ' '.join(pdescr[1:])
				
				self._write_description(pnamelist + pdescr + nl, all_param_names)
				
				HTML.close_tag()
			
		HTML.close_tag()
	
	def _write_predicate_details(self):
		nl = pcsts.nl
		refmaker = lambda s: s.replace('/', '-')
		HTML = self._hw
		
		HTML.open_h2()
		HTML.open_a({'name' : 'details'})
		HTML.put('Predicate Details:')
		HTML.close_tag()
		HTML.close_tag()
		HTML.open_unordered_list({'id' : 'predicate_details'})
		
		# iterate over all blocks
		for binfo in self._class_blocks['predicate']:
			
			label = binfo.get_predicate_label()
			name = binfo.get_predicate_name()
			params = binfo.get_parameters()
			all_param_names = binfo.get_predicate_param_list()
			href = refmaker(label)
			
			HTML.open_list_element()
			PD.pred_title_format(HTML, label,href)
			
			HTML.open_description_list()
			
			# write predicate form
			self._write_pred_form(binfo, name, all_param_names)
			
			# write predicate description
			self._write_pred_descr(binfo, all_param_names)
			
			# write predicate constraints
			if binfo.get_cstrs_descr() != '' or len(params) > 0:
				self._write_pred_constrs(binfo, all_param_names, params)
			
			HTML.close_tag()	# description list
			HTML.close_tag()	# list element
		
		HTML.close_tag() # unordered list
	
	def _write_footer(self):
		HTML = self._hw
		
		HTML.horizontal_line()
		HTML.open_paragraph()
		HTML.open_a({'href' : 'http://github.com/lluisalemanypuig/docyourprolog.git'})
		HTML.put('Generated with DYP')
		HTML.close_tag()
		HTML.close_tag()
	
	def _write_body(self):
		nl = pcsts.nl
		HTML = self._hw
		
		HTML.open_body()
		FD.file_title(HTML, self._short_name)
		
		if 'file' in self._class_blocks != None:
			file_descr = self._class_blocks['file'][-1]
			if file_descr.get_descr() != '':
				self._write_description(file_descr.get_descr(), [])
			if file_descr.get_author() != '':
				FD.file_author(HTML, file_descr.get_author())
			if file_descr.get_date() != '':
				FD.file_date(HTML, file_descr.get_date())
		
		if self._conf.FILE_INCLUSION_GRAPH and self._needs_graph:
			short_name, _ = utils.path_ext(self._short_name)
			HTML.add_image({'name' : short_name + '.png', 'alt' : 'file_inclusion_map'})
		
		if len(self._included_files) > 0:
			self._write_included_files_list()
		
		if 'predicate' in self._class_blocks:
			self._write_predicate_list()
			self._write_predicate_details()
		
		self._write_footer()
		HTML.close_tag()
	
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
		
		self._pred_names = fp.get_predicate_names()
		
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
			WE.absolute_path_not_set(self._abs_name)
			exit(1)
		
		self._hw = hwriter(self._abs_html_name)
		
		self._hw.start()
		self._write_head()
		self._write_body()
		self._hw.close_tag()

