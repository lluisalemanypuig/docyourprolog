
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
	
	def _parse_parameter(self, param):
		# extract parameter type
		opened_bracket = param.find('[')
		closed_bracket = param.find(']')
		param_type = param[opened_bracket:closed_bracket]
		# find starting of description
		s = param.find(' ')
		# variable to store description 
		descr = None
		# find position of next @param
		p = param.find('@param', 1)
		
		if p == -1: descr = param[(s+1):len(param)]
		else: descr = param[(s+1):(p-1)]
		
		print "Description of parameter:",descr
		
	def _add_info(self, environment, info):
		if environment == "form":
			self._form = info[6:len(info)]
			print self._form
		elif environment == "descr":
			self._descr = info[7:len(info)]
			print self._descr
		elif environment == "constr":
			print "constraint info:", info
			
			# space after @constraints
			s = info.find(' ')
			# position of first @param
			p = info.find('@param')
			
			print s,p
			
			# get constraints description
			self._constr = info[(s+1):(p-1)]
			
			print "Constraint description:", self._constr
			
			# delete leading description
			info = info[p:len(info)]
			
			print "Result of deleting leading description:"
			print info
			
			# extract all parameter description
			while len(info) > 0:
				info = self._parse_parameter(info)
				
	def __init__(self, block):
		print "predicate documentation"
		
		self._form = None	# form of the predicate
							# namely, @form
		self._constr = None	# description of constraints
		self._params = []	# parameters of the predicate
							# namely, @constraints
		self._descr = None	# description of the predicate
							# namely, @descr
		
		envir = ""
		info = ""
		
		formpos = (block.find('@form'), 'form')
		descrpos = (block.find('@descr'), 'descr')
		constrspos = (block.find('@constrs'), 'constr')
		
		info = sorted([constrspos, formpos, descrpos])
		
		print info
		
		for i in range(0, len(info)):
			print "++++++++++++++++"
			M = -1
			if i == len(info) - 1: M = len(block)
			else: M = info[i + 1][0] - 1
			
			content = block[info[i][0] : M]
			print content
			
			self._add_info(info[i][1], content)