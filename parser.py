import re

class Parser :

	@staticmethod
	def entities(i) :
		return re.findall(r"{.*?}", i)
		# regex = re.compile(r"{.*?}")
		# if(regex.search(i) != None) :
		# 	extract = regex.search(i).group().split(" ")
		# 	return extract
		# return None
	@staticmethod
	def entities_alt(i) :
		return re.findall(r"{{.*?}}", i)

	@staticmethod
	def commands(i) :
		regex = re.compile(r"<.*?>")
		if(regex.search(i) != None) :
			extract = regex.search(i).group().split(" ")
			return extract
		return None

	@staticmethod
	def actions(i) :
		return re.findall(r"<<.*?>>", i)

	@staticmethod
	def profilers(i) :
		return re.findall(r"\[.*?\]", i)
		# regex = re.compile(r"\[.*?\]")
		# if(regex.search(i) != None) :
		# 	extract = regex.search(i).group().split(" ")
		# 	return extract
		# return None

	@staticmethod
	def modifiers(i) :
		return re.findall(r"\(.*?\)", i)
		# regex = re.compile(r"\(.*?\)")
		# # regex = re.compile(r"(\((?:\(??[^\(]*?\)))")
		# if(regex.search(i) != None) :
		# 	extract = regex.search(i).group().split(" ")
		# 	return extract
		# return None

if __name__ == '__main__':
	print(Parser.profilers("[yes][no]"))
