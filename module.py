from predict import Predict

class Module :
	def __init__(self) :
		self.predictions = []

	def predict(self, pred = "good morning") :
		for p in self.predictions :
			n = Predict(p)
			if n.evaluate(pred) == True :
				return True
		return False