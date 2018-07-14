import utils

"""
PREDICATE DOCUMENTATION
/**
    @form predicate(P1,P2,P3,P4,P5,P6,P7,P8,P9,P10)
    @constraints [Optional description]
		@param P1 blah blah blah
		@param P2 blah blah blah
		@param[++] P3 blah blah blah
		@param[+] P4 blah blah blah
		@param[-] P5 blah blah blah
		@param[--] P6 blah blah blah
		@param[?] P7 blah blah blah
		@param[:] P8 blah blah blah
		@param[@] P9 blah blah blah
		@param[!] P10 blah blah blah
    @descr True if Value is a member of List
*/

All the '@param' are optional.

for more information on parameter 'type', see
http://www.swi-prolog.org/pldoc/man?section=preddesc

"""

class predicate_block:
	
	all_param_types = ["++", "+", "-", "--", "?", ":", "@", "!"]
	
	def _parse_parameter(self, info):
		# find position of next @param
		p = info.find('@param', 1)
		param = None
		if p == -1: param = info
		else: param = info[0:(p-1)]
		
		# extract parameter type
		ob = param.find('[')	# opened bracket
		cb = param.find(']')	# closed bracket
		if ob != -1 and cb != -1: parameter_type = param[(ob+1):cb]
		else: parameter_type = None
			
		# find starting of description
		s = param.find(' ')
		# variable to store description 
		descr = utils.line_cleanup(param[(s+1):len(param)])
		
		# parameter name
		parameter_name = descr.split(' ')[0]
		# parameter constraint information
		self._params[parameter_name] = (parameter_type, descr)
		
		if p == -1: return ""
		return info[p:]
		
	def _add_info(self, environment, info):
		if environment == "form": self._form = info[6:len(info)]
		elif environment == "descr": self._descr = info[7:len(info)]
		elif environment == "constr":
			# space after @constraints
			s = info.find(' ')
			# position of first @param
			p = info.find('@param')
			
			if p == -1:
				# there are no @param -> extract description only
				self._constr = info[(s+1):len(info)]
			else:
				# get constraints description
				self._constr = info[(s+1):(p-1)]
				# delete leading description
				info = info[p:len(info)]
				
				# extract all parameter description
				while len(info) > 0:
					info = self._parse_parameter(info)
		else:
			# this should not happen
			print "Internal error: wrong environment", environment
				
	def __init__(self, block, line):
		self._form = None	# Form of the predicate. Namely @form
		self._constr = None	# Description of constraints
		self._params = {}	# Parameters of the predicate. Namely @constraints
		self._descr = None	# Description of the predicate. Namely @descr
		
		form = (block.find('@form'), 'form')
		descr = (block.find('@descr'), 'descr')
		constr = (block.find('@constrs'), 'constr')
		
		info = sorted([constr, form, descr])
		
		for i in range(0, len(info)):
			M = -1
			if i == len(info) - 1: M = len(block)
			else: M = info[i + 1][0] - 1
			
			content = block[info[i][0] : M]
			self._add_info(info[i][1], content)
		
		# string cleanup
		if self._form != None:
			self._form = utils.line_cleanup(self._form)
		if self._descr != None:
			self._descr = utils.line_cleanup(self._descr)
		if self._constr != None:
			self._constr = utils.line_cleanup(self._constr)
		
		# make sure that there are no two @param defining the same parameter
		param_names = set()
		
		for pname, (ptype,descr) in self._params.iteritems():
			if descr != None:
				descr = utils.line_cleanup(descr)
				if pname in param_names:
					print "    Error: at least two @param defining '%s'" % pname
					print "        In block comment starting at line", line
					exit(1)
				else:
					param_names.add(pname)
		
		# make sure that there are at most as many parameters in
		# form as @param there are in @constraints
		if len(self._params) > self._form.count(',') + 1:
			print "    Warning: too many @param in @constrs environment in block"
			print "        starting at line %d" % line
			exit(1)
	
	def get_form(self): return self._form
	def get_predicate_label(self):
		p = self._form.find('(')
		return self._form[0:p] + '/' + str( self._form.count(',') + 1 )
	def get_predicate_name(self):
		p = self._form.find('(')
		return self._form[0:p]
	def get_predicate_param_list(self):
		op = self._form.find('(')
		cp = self._form.find(')')
		full_list = self._form[(op+1):cp]
		return map(utils.string_cleanup, full_list.split(','))
	def get_description(self): return self._descr
	def get_constraints_description(self): return self._constr
	def get_parameters(self): return self._params
	
	def show(self, tab = ""):
		print "%sPredicate block" % tab
		print "%s    Form: '%s' (%s)" % (tab, self._form, self.get_predicate_label())
		print "%s    Description: '%s'" % (tab, self._descr)
		print "%s    Constraints: '%s'" % (tab, self._constr)
		print "%s    Parameters:" % tab
		for param in self._params:
			print "%s        " % tab, param, self._params[param]
