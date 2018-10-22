
class Arytmetyka:
	
	def __init__(self, value, modulo):
		self.__modulo = modulo
		self.__value = value % modulo

	def __add__(self, other):
		new_value = (self.__value + other.__value) % self.__modulo
		return Arytmetyka(new_value, self.__modulo)

	def __sub__(self, other):
		new_value = (self.__value - other.__value) % self.__modulo
		return Arytmetyka(new_value, self.__modulo)

	def __mul__(self, other):
		new_value = (self.__value * other.__value) % self.__modulo
		return Arytmetyka(new_value, self.__modulo)

	def __str__(self):
		return str(self.__value)

	def gcd(self, a, b):
		# kod z wiki, może się przydać jeszcze
		s, old_s = 0, 1
		t, old_t = 1, 0
		r, old_r = b, a

		while r != 0:
			quotient = old_r // r
			old_r, r = r, old_r - quotient * r
			old_s, s = s, old_s - quotient * s
			old_t, t = t, old_t - quotient * t

		print("Bézout coefficients:", old_s, old_t)
		print("greatest common divisor:", old_r)
		print("quotients by the gcd:", t, s)

		print((old_s * t) % b)

	#odwrotność modulo: a*a^-1 = 1 (mod m)
	def inverse(self):
		m = self.__modulo
		a = self.__value
		m0 = m 
		y = 0
		x = 1

		if (m == 1): 
			return 0

		while (a > 1): 
			q = a // m 
			t = m 
			m = a % m 
			a = t 
			t = y 
			y = x - q * y 
			x = t 

		if (x < 0) : 
			x = x + m0 

		return Arytmetyka(x, self.__modulo) 

		
