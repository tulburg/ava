fnlist = {
	"CW" : "current_word",
	"CP" : "current_phrase",
	"FW" : "first_word",
	"FP" : "first_phrase",
	"NW" : "next_word",
	"NP" : "next_phrase",
	"NWON" : "next_word_or_nothing",
	"NPON" : "next_phase_or_nothing",
	"PW" : "previous_word"
}
def current_word(p, i, arg) :
	return p[i] == arg 
def current_phrase(p, i, arg) :
	for index in range(10) :
		if p[i:index] != arg[index] :
			return False
	return True
def first_word(p, i, arg) :
	return (i == 0) and (p[i] == arg)
def first_phrase(p, i, arg) :
	if i == 0 :
		arg = arg.split(" ")
		for index in range(len(arg)):
			if p[index] != arg[index] :
				return False
		return True
	else :
		return False
def next_word(p, i, arg) :
	if i < len(p) - 1  :
		return p[i+1] == arg
	else :
		return False
def next_phrase(p, i, arg) :
	if i < len(p) - 1 :
		for index in range(10) :
			if p[i:index] != arg[index] :
				return False
		return True
	else :
		return False
def next_word_or_nothing (p, i, arg) :
	if i < len(p) - 1  :
		return p[i+1] == arg
	return True
def next_phrase_or_nothing(p, i, arg) :
	if i < len(p) - 1 :
		for index in range(10) :
			if p[i:index] != arg[index] :
				return False
	return False
def previous_word(p, i, arg) :
	if i > 0 :
		return p[i-1] == arg
	else :
		return False
 