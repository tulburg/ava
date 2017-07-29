import data.prediction_map as pred_map
from parser import Parser
import re
from libs.predict_fnlist import *

class Predict :
	def __init__(self, pred):
		self.extracted = []
		self.pred = pred
		self.fnlist = fnlist
		self.extract()

	def evaluate(self, l_sen) :
		# iterates pred against sentence (localized)
		i = 0
		ex = 0
		for p in self.extracted :
			key = Parser.profilers(p)[0]
			key = key[1:-1]
			args = Parser.modifiers(p)[0]
			args = args[1:-1]
			if not self.__has_child(args) : 
				for s in args.split("|") :
					# temporary splitting there, adjust for better splitting
					if i < len(l_sen) and globals()[fnlist[key]](l_sen.split(" "), i, s) == True :
						i += len(args.split(" "))
						ex += 1
						if ex == len(self.extracted) :
							return True
					else : 
						print("Got false %d %s" % (ex, s))
			else :
				print("Has child")


	@staticmethod
	def process(pred, l_sen) :
		# iterates pred against sentence (localized)
		for p in pred :
			print(p[4:])
			print(Parser.profilers(p[4:]))

	def extract(self, pred=None) :
		if pred == None : 
			pred = self.pred
		if pred[0] == "[" :
			n = "]"
			if pred[pred.index(n) + 1] == "(" :
				# if its a function
				tot_index = pred.index("(")
				if self.__has_child(pred[tot_index+1:len(pred[:pred.index(")")])]) :
					# count braces
					op = 1
					cl = 0
					cindex = tot_index + 1
					for i in range(10) :
						try:
							if pred[cindex:].index(")") > pred[cindex:].index("(") :
								cindex = cindex + pred[cindex:].index("(") + 1
								op += 1
							else :
								cl += 1
								cindex = cindex + pred[cindex:].index(")") + 1
						except ValueError:
							cindex = cindex + pred[cindex:].index(")") + 1
							cl += 1
						if op == cl or cindex == len(pred) :
							self.extracted.append(pred[:cindex])
							if len(pred[cindex:]) > 0 :
								self.extract(pred[cindex:])
							break
				else :
					tot_index = pred.index(")") + 1
					self.extracted.append(pred[:pred.index(")") + 1])
					if len(pred[tot_index:]) > 0:
						self.extract(pred[tot_index:])
			else :
				self.extracted.append(pred[:pred.index(n)+1])
				self.extract(pred[pred.index(n)+1:])

	def __has_child(self, pred) :
		return next((s for s in pred if s == "("), None) != None 

if __name__ == '__main__':
	p = Predict("[FW](good)[CW](morning|day|afternoon|night)")
	print(p.evaluate("good afternoon"))
