import sys
sys.path.append("/Applications/XAMPP/htdocs/ava/")

from flask import Flask, render_template, request, redirect, url_for
from libs.states import state_object
from data.db import db, vocabulary, matrix as matrixDb
app = Flask(__name__)

data = {
	'index' : { 'status' : 'Welcome to Sentence Synth' },
	'matrix' : { 'status' : 'Welcome to the Matrix!' }
}
data = state_object(**data)

@app.route("/")
def index() :
	return render_template(
		'index.html', data=data.index)

@app.route("/matrix")
def matrix() :
	return render_template(
		'matrix.html', data=data.matrix)

@app.route("/matrix_submit", methods=["POST"])
def matrix_submit() :
	parent = request.form['parent']
	name = request.form['name']
	value = request.form['value']

	matrixDb.set(parent, name, value)
	data.matrix.status = ":: Successfully inserted the matrix"
	return redirect(url_for('matrix'))

@app.route("/word_map_submit", methods=["POST"])
def word_map_submit() :
	key = request.form['key']
	primary = request.form["primary"]
	clippings = request.form['clippings']

	vocabulary.set(key, primary, clippings, "")

	data.index.status = ':: Successfully got the form'
	print(">> Got input : "+str(primary))
	return redirect(url_for('index'))

# @app.route("/handle_submit", methods=["POST"])
# def handle_submit() :
# 	moutput = request.form["output"]
# 	print(":: Got output : "+str(moutput))
# 	data.output.input = moutput
# 	data.output.processed = process_output(moutput)
# 	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8010)