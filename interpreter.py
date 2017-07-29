import data.interpreter_map as data_map
import re
from predict import Predict

class Interprete :
	@staticmethod
	def process(sen) :
		for p in dir(data_map) :
			if str(p)[0] != "_" :
				s = getattr(data_map, p)
				for q in s: 
					for r in s[q] :
						sen = re.sub(r"\b"+r+r"\b", lambda line: match_case(line, q), sen, flags=re.IGNORECASE)
		return sen
	@staticmethod
	def questionate(sen) :
		p = Predict("[FP](what is)[CT]({OBJECT})")
		if p.evaluate(sen) == True :
			rep = re.sub("what is ", "[?]({ANY})", sen)
			print(rep)

	def crunch(sen) :
		# tense (present, future, past)
		# continuity
		# weight (negativity, positivity)
		# measurement (counting)
		# base words
		# incredibly so [50:](go[ING] home tonight)
		# what happened last night [?](happen[pst])(last night)
		# i have 10 cars {self}(has)[10]{car}
		# i'm going home {self}(go[ING]){home}
		something = True



	def test_question(sen) :
		chars = sen.split();
		if chars[1] == "?" :
			return True	
		return False

def match_case(r, a) :
	if r.group(0)[0].isupper() :
		return a.capitalize()
	return a

if __name__ == '__main__':
	Interprete.questionate("what is the time")