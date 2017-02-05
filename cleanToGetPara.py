import os
import re
from nltk.corpus import stopwords

if not os.path.exists('Cleaned scripts'):
	os.mkdir('Cleaned scripts')
for root, directory, files in os.walk('./scripts'):
	for file in files:
		#print(root, directory, file)
		file_path = os.path.join(root, file)
		f = open(file_path, encoding="utf8")
		text = f.read()
		text = re.sub(r'\d\d\:\d\d\n', '', text)
		text = re.sub(r'\n', ' ', text)
		text = re.sub('\s+', ' ', text)

		words = text.split()
		filtered_words = [word for word in words if word not in stopwords.words('english')]
		text = ' '.join(filtered_words)

		dir_ = root.split('\\')[1]
		if not os.path.exists('Cleaned scripts\\'+dir_):
			os.makedirs('Cleaned scripts\\'+dir_)
		file = os.path.join(os.getcwd()+'\\Cleaned scripts\\'+dir_, file)
		fout = open(file, 'w', encoding="utf8")
		fout.write(text)