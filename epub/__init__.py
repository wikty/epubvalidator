import subprocess, os, re

def check(filename, epubcheck_path):
	try:
		output = subprocess.check_output(
			['java', '-jar', epubcheck_path, filename],
			stderr=subprocess.STDOUT,
			shell=True
		)
	except subprocess.CalledProcessError as e:
		output = e.output

	output = output.decode('gbk')
	errors = []
	# regex = re.compile(r'\(\d+,\d+\)')
	for line in output.splitlines():
		# line = str(line).strip('b')
		columns = line.split(': ')
		if len(columns) != 3:
			continue
		error_type = columns[0]
		error_file = os.path.basename(columns[1]).split('(')[0]
		error_message = columns[2]
		error_line, error_position = os.path.basename(columns[1]).split('(')[1].strip(')').split(',')
		errors.append({
			'type': error_type,
			'file': error_file,
			'line': error_line,
			'position': error_position,
			'message': error_message
		})
	return {
		'filename': os.path.basename(filename),
		'errors': errors
	}