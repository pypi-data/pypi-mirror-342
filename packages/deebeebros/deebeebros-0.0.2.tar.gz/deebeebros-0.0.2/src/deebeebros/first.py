import sys

def plus(a, b):
	return a + b

def minus(a, b):
	return a - b

def sul(a, b):
	return a / b

def fromargs():
	i = int(sys.argv[1])
	j = int(sys.argv[2])
	return i * j

def frominput():
	s = input("Dit is de boodschap: ")
	return s.upper()

def tooutput():
	print('prutje')

def bodexit(dus: str):
	sys.exit(1)