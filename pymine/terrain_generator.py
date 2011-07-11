class TerrainGenerator:
	def generate(self,seed,x,y): 
		# generates and returns a chunk. x and y are the chunk coords
		self.blocks = {}
		
		#create bedrock level
		b = 0
		c = 0
		while b<17:
			while c<17:
				self.blocks.append({str(b)+str(c): 7})
			
		