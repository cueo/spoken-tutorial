import os
import re
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['hello', 'spoken', 'tutorial', 'dear', 'friends', 'welcome'])


def simple_clean(text):
	text = text.lower()
	text = re.sub(r'https?:\/\/.*', '', text)
	text = re.sub('/', ' ', text)
	text = re.sub('[#.,$%|~\-&\"\'`*+=!?;(){}^\[\]<>]', '', text)
	text = re.sub('\n+', ' ', text)
	text = re.sub(' +', ' ', text)
	words = [word for word in text.split(' ') if word not in stop_words]
	return ' '.join(words)


def clean(text):
	text = text.lower()
	text = re.sub('[#.,$%|~\-/&\"\'`*+=!?;(){}^]', '', text)
	text = re.sub('\n ', '\n', text)
	text = re.sub('\n+', '\n', text)
	text = re.sub(' +', ' ', text)
	# text = re.sub(r'(\d+:\d+)[ \n]+(((?!\d+:\d+).)*)', r'\1\n\2\n', text, re.S)
	matches = re.findall(r'(\d+:\d+)[ \n]+(((?!\d+:\d+).)*)', text, re.S)

	cleaned_lines = []
	for match in matches:
		timestamp = match[0]
		line = re.sub('\n+', ' ', match[1])

		if 'end of this tutorial' in line:
			break

		line = line.strip()
		line = re.sub(r':([ ]?)', r'\1', line)
		words = line.split(' ')
		filtered_words = [word for word in words if word not in stop_words]
		cleaned_lines.append((' '.join(filtered_words), timestamp))

	return cleaned_lines


def clean_all_scripts(path):
	"""
	Check if all files are getting cleaned.
	Exception shouldn't be thrown for any of the file.
	"""
	for r, d, files in os.walk(path):
		for f in files:
			if f.endswith('.txt'):
				print 'Cleaning file:', f
				file_path = os.path.join(r, f)
				with open(file_path, 'r') as fp:
					try:
						clean(fp.read())
					except Exception as e:
						print "Couldn't clean file:", f
						print 'Reason:', e


if __name__ == '__main__':
	# clean_all_scripts(path)
	path = 'data'
	with open('data/BASH/Advance-topics-in-a-function.txt', 'r') as f:
		print clean(f.read())
