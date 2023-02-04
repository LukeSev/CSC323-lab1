
#Mersenne Twister MT 19937
class MT19937:
	def __init__(self, seed):
		self.W, self.N, self.M, self.R = 32, 624, 397, 31
		self.A = 0x9908B0DF
		self.U, self.D = 11, 0xFFFFFFFF
		self.S, self.B = 7, 0x9D2C5680
		self.T, self.C = 15, 0xEFC60000
		self.L = 18
		self.F = 1812433253

		self.MT = [0] * self.N
		self.index = (self.N) + 1
		self.lower_mask = (1 << self.R) - 1
		self.upper_mask = self.int_bits(~self.lower_mask) # Take lowest W bits of not lower mask

		self.seed_MT(int.from_bytes(seed, "big"))
		return

	def int_bits(self, num):
		return int(0xFFFFFFFF & num)

	def seed_MT(self, seed):
		self.index = self.N
		self.MT[0] = seed
		for i in range(1, self.N):
			intermed = (self.F * (self.MT[i-1] ^ (self.MT[i-1] >> (self.W-2))) + i)
			self.MT[i] = self.int_bits(intermed) # Lowest W bits of intermediate var

	def twist(self):
		for i in range(self.N):
			xUpper = (self.MT[i] & self.upper_mask)
			xLower = self.MT[(i+1) % self.N] & self.lower_mask
			# x = xUpper concatenated with xLower
			x = self.int_bits((xUpper << self.R) | xLower)

			xA = x >> 1
			if((x % 2) != 0):
				xA = xA ^ self.A
            
			self.MT[i] = self.MT[(i + self.M) % self.N] ^ xA
		self.index = 0

	def extract_number(self):
		if(self.index >= self.N):
			if(self.index > self.N):
				print("Error: Generator was never seeded")
			#self.twist()
			self.generate_number()

		y = self.MT[self.index]
		y = y ^ ((y >> self.U))
		y = y ^ ((y << self.S) & self.B)
		y = y ^ ((y << self.T) & self.C)
		y = y ^ (y >> self.L)

		self.index += 1
		return self.int_bits(y)

	def generate_number(self):
		# Since it said "Mix state here," I'm assuming this is analogous to my twist() function
		for i in range(self.N):
			xUpper = (self.MT[i] & self.upper_mask)
			xLower = self.MT[(i+1) % self.N] & self.lower_mask
			# x = xUpper concatenated with xLower
			x = self.int_bits((xUpper << self.R) | xLower)

			xA = x >> 1
			if((x % 2) != 0):
				xA = xA ^ self.A
            
			self.MT[i] = self.MT[(i + self.M) % self.N] ^ xA
		self.index = 0
		

