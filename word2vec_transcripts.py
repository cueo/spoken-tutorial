from gensim.models import Word2Vec
import os
from preprocess import clean

class CleanSentences:
	def __init__(self, path):
		self.path = path

	def __iter__(self):
		for r, d, files in os.walk(self.path):
			for f in files:
				if f.endswith('.txt'):
					file_path = os.path.join(r, f)
					with open(file_path, 'r') as fp:
						clean_text = clean(fp.read())
						for x in clean_text:
							yield x[0].split()

if __name__ == '__main__':
	sentences = CleanSentences('data')
	print 'Creating a word2vec model for the transcripts...'
	model = Word2Vec(sentences, size=dimension)
	model.save('data/snippet.model')
	print 'Created a word2vec model for the transcripts.'
		
