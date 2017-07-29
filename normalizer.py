import re
import textacy
import time

class Normalize :

	def __init__(self) :
		self.started = True
	@staticmethod
	def expand(data) :
		with open('data/expansion_map.txt', 'r+') as fp :
			for i,line in enumerate(fp) :
				mapped = line[:-1].split("=")
				subs = mapped[1].split(",")
				for sub in subs :
					data = re.sub(r"\b"+re.escape(sub)+"\\b", lambda line: match_case(line, mapped[0]), data, flags=re.I)
		return data

	@staticmethod
	def lemmanize(data) :
		doc = textacy.Doc(data, lang="en")
		pattern = textacy.constants.POS_REGEX_PATTERNS['en']['NP']
		v_pattern = textacy.constants.POS_REGEX_PATTERNS['en']['VP']
		objs = list(textacy.extract.pos_regex_matches(doc, pattern))
		verbs = list(textacy.extract.pos_regex_matches(doc, v_pattern))
		prons = list(textacy.extract.pos_regex_matches(doc, r'<PRON>'))
		with open('data/base_word_map.txt', 'r+') as fp :
			for i,line in enumerate(fp) :
				mapped = line[:-1].split("=")
				subs = mapped[1].split(",")
				for sub in subs :
					# +"(.*?)$"
					data = re.sub(r"\b"+re.escape(sub)+"\\b", lambda m: re_replace(m, data, mapped[0]), data)
					data = re.sub(r"~.*?$", "", data)
		for s in objs :
			data = re.sub(r"\b"+re.escape(str(s))+"\\b", lambda m: su_replace(m, str(s), "{", "}"), data)
		for p in prons :
			data = re.sub(r"\b"+re.escape(str(p))+"\\b", lambda m: su_replace(m, str(p), "{{", "}}"), data)
		for t in verbs :
			data = re.sub(r"\b"+re.escape(str(t))+"\\b", lambda m: su_replace(m, str(t), "[", "]"), data)
		return data

def su_replace(m, s, su1, su2) :
	return su1+s+su2

def re_replace(s, d, m) :
	s = s.group(0)
	return m+"("+d[(d.index(s)+len(s)):].strip()+")~"
	# return m+"("
def match_case(r, a) :
	if r.group(0)[0].isupper() :
		return a.capitalize()
	return a

if __name__ == '__main__':
	s = Normalize()
	print(s.lemmanize(s.expand("how is tolu doing")))