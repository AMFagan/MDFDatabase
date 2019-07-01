import PyPDF2

with open('MDFs/MM113-MDF.pdf', 'rb') as pdf:
	reader = PyPDF2.PdfFileReader(pdf)
	out = (reader.getPage(0).extractText())
	out = out.replace(u'\u2122', '\'')
	with open('output.txt', 'w') as outfile:
		for l in out.split('\n'):
			outfile.write(l)


