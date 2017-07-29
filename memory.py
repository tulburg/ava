from sqlalchemy import *

class Memory :
	def __init__(self) :
		self.__started__ = True

	# triangulator
	def triangulate(self, p) :
		""" 
		Triangulate a piece of memory to search for 
		behavioural patterns in the memory behavioural
		matrix
		@param p : the piece of memory to triangulate
		"""

		#first: fetch p with parent pieces from a week or longer
		#second: map p with parent pieces respectively
		#third: search for mapped results in memory matrix
		#fourth: return mapped results (id, weight and value)




