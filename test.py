from parser import Parser

def levenshtein(s, t):
        ''' From Wikipedia article; Iterative with two matrix rows. '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(t)]

def match(a, b) :
	if a.__contains__("...") :
		i = a.index("...")
		if i == 0 :
			aa = a[3:]
			if aa.__contains__("...") :
				aa = aa[:-3]
				if b.__contains__(aa) and b.index(aa) != 0 and b.index(aa) != len(b[:-len(aa)]):
					pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
					return (True, pro)
				else :
					pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
					return (False, pro)
			elif b.__contains__(aa) :
				pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
				if b.__contains__(aa) and b.index(aa) == len(b[:-len(aa)]):
					return (True, pro)
				else :
					return (False, pro)
		elif i == len(a[:-3]) :
			aa = a[:-3]
			pro = (len(aa.split(" ")) + len(Parser.profilers(aa))) / (len(b.split(" ")) + len(Parser.profilers(b)))
			if b.__contains__(aa) and b.index(aa) == 0:
				return (True, pro)
			else :
				return (False, pro)
	else :

		pro = (len(a.split(" ")) + len(Parser.profilers(a))) / (len(b.split(" ")) + len(Parser.profilers(b)))
		if b.__contains__(a) and b.index(a) != len(b[:-len(a)]):
			return (True, pro)
		else :
			return (False, pro)

print(match("...[work]...", "[best][work][please]"))