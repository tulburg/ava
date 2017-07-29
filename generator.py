import re
from data.db import vocabulary
from libs.utils import Logger


class Generator:
	def __init__(self) :
		self.__started__ = True
	def speech(self, command, clippings = None) :
		sentence = ""
		cont = True
		while(cont) :
			extract = re.findall(r".*?\(", command)
			if len(extract) > 0 :
				for fns in extract :
					sentence += self._lookup(fns[:-1], 20)+", "
					new_command = command[:-1]
					command = re.sub(re.escape(fns), "", new_command)
			else :
				sentence += self._lookup(command, 20)+" "
				cont = False
		log(sentence)
		return sentence

	def _lookup(self, command, lexprof) :
		lookup = vocabulary.get(command)
		if len(lookup) > 0 :
			sent = lookup[0].primary_value
			temp_key = 0
			for s in sent.split(",") :
				new_key = int(s.split(":")[0].strip())
				if lexprof > temp_key and lexprof <= new_key :
					temp_key = new_key
					return s.split(":")[1].strip()
		return "*"+command+"*"

log = Logger(Generator).log

if __name__ == '__main__':
	log(Generator().speech("sorry([cant][remember])"))
	log(Generator().speech("sorry([cant][remember]([meet](<<you>>)))"))