import os, subprocess, json

from flask import Flask, render_template, url_for, redirect, session, escape, request
from werkzeug.utils import secure_filename

from utils import post_file, is_allowed_file
from epub import check

currentdir = os.path.abspath(os.getcwd())
config = {
	'sitename': 'Epub-Validator',
	'upload_field': 'file[]',
	'epubcheck_path': os.sep.join([currentdir, 'bin', 'epubcheck-4.0.1', 'epubcheck.jar']),
	'upload_folder': os.sep.join([currentdir, 'upload']),
	'allowed_extensions': set(['epub'])
}

app = Flask(__name__)
# In order to use sessions you have to set a secret key
app.secret_key = '\x8e\xcc\x82\x13X\xcc!2\x08(\xb1\x14\xfc\xd0\x93\x97\x1d\xce6\xa8(\xb3>*' # os.urandom(24)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB upload max size


@app.route('/', methods=['GET'])
def index():
	return render_template(
		'index.html', 
		upload_url=url_for('upload'),
		upload_field=config['upload_field'])

@app.route('/upload', methods=['POST'])
def upload():
	results = []

	files = []
	for file in request.files.getlist(config['upload_field']):
		if file and file.filename and is_allowed_file(file.filename, config['allowed_extensions']):
			filename = secure_filename(file.filename)
			filename = os.path.join(config['upload_folder'], filename)
			file.save(filename)
			files.append(filename)

	for filename in files:
		result = check(filename, config['epubcheck_path'])
		results.append(result)
	
	session['results'] = json.dumps(results, ensure_ascii=False)
	# return redirect(url_for('validate', results=results))
	return redirect(url_for('validate'))

@app.route('/validate')
def validate():
	# results = request.args['results']
	if 'results' not in session:
		return redirect(url_for('index'))
	results = session['results']
	return render_template('validate.html', results=json.loads(results))

if __name__ == '__main__':
	with app.test_client() as client:
		post_file(client, 'epub/test.epub', '/upload')