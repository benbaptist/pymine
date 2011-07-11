class TerrainGenerator:
	def __init__(self, seed):
		self.seed = seed
	
	def generate(self, x, y): 
		# Generates and returns a chunk. x and y are the chunk coords
		self.blocks = {}
		
		# Create bedrock level
		b = 0
		c = 0
		while b < 17:
			while c < 17:
				self.blocks.append({str(b) + str(c): 7})
