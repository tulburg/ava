from module import Module

class Greetings(Module) :
	def __init__(self) :
		super()
		self.predictions = [
			"[FW]((hello|hey|hi)[NWON]([ref:place]))",
			"[FW](good)[CW](morning|day|afternoon|night)",
			"[FW](bye|goodbye)",
			"[FP](top of the (morning|day))"
		]

		print(self.predict("good morning".split(" ")))

if __name__ == '__main__':
	g = Greetings()

