class HexToDecimal:
	def __init__(self,hexadecimal):
		a = 0
		self.b = ""
		self.c = []
		for x in hexadecimal:
			a += 1
			if a % 2 == 0:
				self.b += x
				self.c.append(self.b)
				self.b = ""
			else:
				self.b += x
		d = 0
		for x in self.c:
			if x == "01":
				d += 1
			if x == "02":
				d += 2
			if x == "03":
				d += 3
			if x == "04":
				d += 4
			if x == "05":
				d += 5
			if x == "06":
				d += 6
			if x == "07":
				d += 7
			if x == "08":
				d += 8
			if x == "09":
				d += 9
			if x == "0a":
				d += 10
			if x == "0b":
				d += 11
			if x == "0c":
				d += 12
			if x == "0d":
				d += 13
			if x == "0e":
				d += 14
			if x == "0f":
				d += 15
		self.result = d
class DecimalToHex: # WARNING: DOES NOTHING DIFFERENT THAN HextoDecimal!
	def __init__(self,hexadecimal):
		a = 0
		self.b = ""
		self.c = []
		for x in hexadecimal:
			a += 1
			if a % 2 == 0:
				self.b += x
				self.c.append(self.b)
				self.b = ""
			else:
				self.b += x
		d = 0
		for x in self.c:
			if x == "01":
				d += 1
			if x == "02":
				d += 2
			if x == "03":
				d += 3
			if x == "04":
				d += 4
			if x == "05":
				d += 5
			if x == "06":
				d += 6
			if x == "07":
				d += 7
			if x == "08":
				d += 8
			if x == "09":
				d += 9
			if x == "0a":
				d += 10
			if x == "0b":
				d += 11
			if x == "0c":
				d += 12
			if x == "0d":
				d += 13
			if x == "0e":
				d += 14
			if x == "0f":
				d += 15
		self.result = d
			
	
			
#poo = HexToDecimal("224422442244")
#print poo.c