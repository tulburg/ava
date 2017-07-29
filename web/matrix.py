from flask import Flask, render_template, request, redirect, url_for
import sys

sys.path.append("/Applications/XAMPP/htdocs/ava/")

#Now my own imports
from interpreter import Interprete
from normalizer import Normalize
from libs.utils import util
import textacy

app = Flask(__name__)

minput = util.dict_to_obj({
	"input" : "",
	"nounp" : "",
	"verbp" : "",
	"pos_tags" : ""
})
moutput = util.dict_to_obj({
	"input" : "",
	"processed" : ""
})
data = util.dict_to_obj({
	"input" : minput,
	"output": moutput
})

def process_input(m) :
	m_norm = Normalize.expand(m)
	m_inter = Interprete.process(m_norm)
	doc = textacy.Doc(m_norm)
	pattern = textacy.constants.POS_REGEX_PATTERNS['en']['NP']
	pattern_2 = textacy.constants.POS_REGEX_PATTERNS['en']['VP']
	nn = str(list(textacy.extract.pos_regex_matches(doc, pattern)))
	vv = str(list(textacy.extract.pos_regex_matches(doc, pattern_2)))
	data.input.input = m_norm
	data.input.nounp = nn
	data.input.verbp = vv
	# data.input.pos_tags = str(doc.pos_tagged_text)
	data.input.pos_tags = Normalize.lemmanize(m_norm)

def process_output(m) :
	#just return m for now
	return m

@app.route("/")
def index() :
	return render_template(
		'layout.html', data=data)

@app.route("/handle_input", methods=["POST"])
def handle_input() :
	minput = request.form["input"]
	print(">> Got input : "+str(minput))
	process_input(minput)
	return redirect(url_for('index'))

@app.route("/handle_submit", methods=["POST"])
def handle_submit() :
	moutput = request.form["output"]
	print(":: Got output : "+str(moutput))
	data.output.input = moutput
	data.output.processed = process_output(moutput)
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8010)



