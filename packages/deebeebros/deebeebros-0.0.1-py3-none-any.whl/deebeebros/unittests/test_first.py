import sys
from base_test import BaseTest

class RunTest(BaseTest):
	def mandatory_functions(self):
		return ['plus', 'minus', 'sul', 'fromargs', 'frominput', 'tooutput', 'bodexit']

	# ordering by alphabet
	def test_a_plus(self):
		funcname = 'plus'
		testname = f'This function receives two numbers as paramaters a and b, it returns the sum of a + b.'
		expected = 5
		parameters = (2, 3)
		comargs = []
		self.assert_params_comargs(funcname, testname, expected, parameters, comargs)
		expected = -12
		parameters = (-20, 9)
		self.assert_params_comargs(funcname, testname, expected, parameters, comargs)

	def test_b_sul(self):
		funcname = 'sul'
		testname = 'This function should catch the ZeroDivisionError exception and return 0, if trying to divide by zero.'
		expected = 3
		parameters = (3, 1)
		comargs = []
		self.assert_params_comargs(funcname, testname, expected, parameters, comargs)
		expected = 0
		parameters = (3, 0)
		self.assert_params_comargs(funcname, testname, expected, parameters, comargs)

	def test_c_sul_nul(self):
		funcname = 'sul'
		testname = 'This function should catch the ZeroDivisionError exception and return 0, if trying to divide by zero.'
		expected =  'ZeroDivisionError'
		parameters = (4, 0)
		comargs = []
		# self.btc.assert_params_comargs(funcname, testname, expected, parameters, comargs)
		self.raise_error(funcname, testname, expected, parameters, comargs)

	def test_d_fromargs_ok(self):
		funcname = 'fromargs'
		testname = ''
		expected = 15
		parameters = tuple()
		comargs = ['3', '5']
		self.assert_params_comargs(funcname, testname, expected, parameters, comargs)

	def test_e_fromargs_nul(self):
		funcname = 'fromargs'
		testname = ' with not enough command line arguments'
		expected = 'IndexError'
		parameters = tuple()
		comargs = ['3']
		self.raise_error(funcname, testname, expected, parameters, comargs)

	def test_f_frominput(self):
		funcname = 'frominput'
		expected = 'BOEF'
		parameters = tuple()
		comargs = []
		erin = "Boef"
		testname = f' where user input would be "{erin}"'
		self.input_and_or_output(funcname, testname, expected, parameters, comargs, erin=erin)

	def test_g_tooutput(self):
		funcname = 'tooutput'
		expected = 'prutje'
		parameters = tuple()
		comargs = []
		eruit = expected
		testname = f' where prompt output should be "{eruit}"'
		self.input_and_or_output(funcname, testname, expected, parameters, comargs, eruit=eruit)

	def test_h_must_exit(self):
		funcname = 'bodexit'
		expected = 1
		parameters = ('dusss',)
		comargs = []
		testname = f' should exit with message "{expected}"'
		self.sys_exit(funcname, testname, expected, parameters, comargs)
