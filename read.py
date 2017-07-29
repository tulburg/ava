from lxml import html
import requests
import re
from normalizer import Normalize
from interpreter import Interprete
import textacy


import urllib
from bs4 import BeautifulSoup

# url = "https://en.wikipedia.org/wiki/Place"
# html = urllib.urlopen(url).read()

page = requests.get("https://en.wikipedia.org/wiki/Place")
c = page.content.decode('UTF-8')
soup = BeautifulSoup(c, "lxml")
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())

# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

# text = text.split(r"[\n|\t]*")

print(str(text))



# page = requests.get("https://en.wikipedia.org/wiki/Place")
# c = str(page.content)
# rep = re.sub(r"<[^>]*>", "", c)
# rep = re.sub(r"\\[^*]", "", rep)
# rep = re.sub(r"([^*#\s]*\.[^*#\s]{1,})", "", rep)
# s = re.split(r"\.|\?", rep)
# print(rep)




s = "There's a reason i decided not to come to the wedding with you. And I still stand by the decision. I am not interested in the idea of a one night stand, so am telling you right now not to poke the wrong tree. It's bad enough that he thinks am not a good person, but for you to change the capet without my consent is just below the belt"
meta = {
	"title" : "Funny Story",
	"author" : "tolu oluwagbemi",
	"pub_date" : "12 June '17"
}
# include 's
# possessive = ["of", "has", "my", "our", "her", "his", "their", "your"] 
# direct = ["is"]
# referers = ["he", "she", "i", "they", "us", "you", "am"]
# pointers = ["a", "the"]

objects = []
s_norm = Normalize.expand(s)
s_inter = Interprete.process(s_norm)

# s_splitted = re.split(r"[\s\.\,]", s_norm)
# m_splitted = re.split(r"[\s\.\,]", s_inter)

print(s_norm)
doc = textacy.Doc(s_norm, metadata = meta)
pattern = textacy.constants.POS_REGEX_PATTERNS['en']['NP']
pattern_2 = textacy.constants.POS_REGEX_PATTERNS['en']['VP']
pattern_3 = textacy.constants.POS_REGEX_PATTERNS['en']['PP']

# print(list(textacy.extract.ngrams(doc, 3, filter_stops=True, filter_punct=True, filter_nums=False)))
print(list(textacy.extract.pos_regex_matches(doc, pattern)))
print(list(textacy.extract.pos_regex_matches(doc, pattern_2)))
# print(list(textacy.extract.pos_regex_matches(doc, pattern_3)))

# print(list(doc.to_terms_list(ngrams=1, named_entities=True, as_strings=True, normalize=False)))


# for i in range(len(s_splitted)) :
# 	if m_splitted[i] == "{ref:direct}" :
# 		objects.append(s_splitted[i+1])

# print(objects)

		







