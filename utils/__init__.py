import io

def is_allowed_file(filename, extensions=set()):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def post_file(app_client, fname, url):
	with open(fname, 'rb') as f:
		app_client.post(url, data={'file': (io.BytesIO(f.read()), fname)})