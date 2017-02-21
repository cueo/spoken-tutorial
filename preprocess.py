from __future__ import print_function
import os
import re
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend(['hello', 'spoken', 'tutorial', 'dear', 'friends', 'welcome'])


def clean(text):
	text = text.lower()
	text = re.sub('[#.,$%|~\-/&\"\'`*+=!?;()^]', '', text)
	text = re.sub('\n ', '\n', text)
	text = re.sub(' +', ' ', text)

	lines = text.split('\n\n')
	found = False
	for index, line in enumerate(lines):
		if 'end of this tutorial' in line:
			found = True
			break
	if found:
		lines = lines[:index]

	cleaned_lines = []
	for line in lines:
		details = line.split('\n')
		timestamp, words = details[0], details[1]
		words = words.split(' ')
		filtered_words = [word for word in words if word not in stop_words]
		cleaned_lines.append((' '.join(filtered_words), timestamp))

	return cleaned_lines


def main():
	clean_dir = 'scripts/clean/'
	if not os.path.exists(clean_dir):
		os.mkdir(clean_dir)

	for root, directory, files in os.walk('./scripts'):
		if '.DS_Store' in files:
			files.remove('.DS_Store')
		if 'clean' not in root.split(os.sep):
			for file in files:
				file_path = os.path.join(root, file)
				print('Cleaning:', file_path.split(os.sep, maxsplit=2)[-1])
				f = open(file_path, encoding='utf8')
				text = f.read()
				f.close()
				text = clean(text)

				dir_ = root.split(os.sep)[1]
				if not os.path.exists(clean_dir + dir_):
					os.makedirs(clean_dir + dir_)
				file = os.path.join(os.getcwd(), clean_dir, dir_, file)
				fout = open(file, 'w', encoding='utf-8')
				fout.write(text)
				fout.close()


if __name__ == '__main__':
	# main()
	with open('scripts/BASH/Introduction-to-BASH-Shell-Scripting.txt', 'r') as f:
		file_text = f.read()
	clean(file_text)