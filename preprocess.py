import os
import re
from nltk.corpus import stopwords

clean_dir = 'scripts/clean/'

if not os.path.exists(clean_dir):
	os.mkdir(clean_dir)

for root, directory, files in os.walk('./scripts'):
	if '.DS_Store' in files:
		files.remove('.DS_Store')
	if root.split(os.sep)[-2] != 'clean':
		for file in files:
			file_path = os.path.join(root, file)
			print('Cleaning:', file_path.split(os.sep, maxsplit=2)[-1])
			f = open(file_path, encoding='utf8')
			text = f.read()
			f.close()
			text = text.lower()
			text = re.sub(r'\d\d\:\d\d\n', '', text)
			text = re.sub('[#.,$%|~\-\/&\"\'`*+=!?;:()^]', '', text)
			text = re.sub(r'\n', ' ', text)
			text = re.sub('\s+', ' ', text)

			words = text.split()
			filtered_words = [word for word in words if word not in stopwords.words('english')]
			text = ' '.join(filtered_words)

			dir_ = root.split(os.sep)[2]
			if not os.path.exists(clean_dir + dir_):
				os.makedirs(clean_dir + dir_)
			file = os.path.join(os.getcwd(), clean_dir, dir_, file)
			fout = open(file, 'w', encoding='utf-8')
			fout.write(text)
			fout.close()