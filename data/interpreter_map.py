wh = {
	"[?person]" : ["who", "whom"],
	"[?thing]" : ["what"],
	"[?place]" : ["where"],
	"[?method]" : ["how"],
	"[?time]" : ["when"],
	"[?reason]" : ["why"]
}

""""
	key :
		ref = reference
		ptr = pointer
		clr = classifier
"""
pointer_map = {
	"{ref:self:possessive}" : ["my"],
	"{ref:self}" : ["myself", "me", "i", "am"],
	"{ref:direct}" : ["the", "a"],
	"{ref:th:s}" : ["that", "this"],
	"{ref:th:p}" : ["those", "these"],
	"{ref:place}" : ["there"],
	"{ref:possessive}" : ["of"],
	"{ptr:direct:s}" : ["is"],
	"{ptr:direct:p}" : ["are"],

	"{clr:indirect}" : ["like", "as"],


	"{ref:object}" : ["it", "its", "itself"],
	"{ref:third_person_plural}" : ["their", "theirs", "them", "themselves", "they"],
	"{ref:third_person}" : ["him", "his", "her", "herself", "himself"],

	"{ref:other}" : ["you", "your", "yourself"]
}