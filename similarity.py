# -*- coding: utf-8 -*-

import re
import nltk, string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import manhattan_distances
from gensim.models import Word2Vec


class Similarity():
	stemmer = nltk.stem.porter.PorterStemmer()
	remove_punctuation_map = dict((ord(char), None) for char in string.punctuation + '“”[](){}')
	stop_words = stopwords.words('english')
	stop_words.extend([])

	def __init__(self, documents):
		self.documents = documents
		self.clean()
		self.vectorizer = TfidfVectorizer(tokenizer=self.normalize, stop_words='english')
		self.tfidf = self.vectorizer.fit_transform(self.documents)

	def clean(self):
		for i in xrange(len(self.documents)):
			document = self.documents[i]
			document = re.sub('\n+', '\n', document)
			document = re.sub('[#.,$%|~\-\/&\"\'`*+=!?;:()^“”]', '', document)
			document = document.lower()
			for word in self.stop_words:
				document = re.sub(r'\b' + word + r'\b', '', document)
			document = re.sub(' +', ' ', document)
			self.documents[i] = re.sub(r'\n ', '\n', document)

	def word2vec(self):
		sentences = []
		for document in self.documents:
			sentences.extend(document.split('\n'))
		model = Word2Vec(sentences, window=5, size=64, iter=100)
		model.save('model')

	def stem_tokens(self, tokens):
		return [self.stemmer.stem(item) for item in tokens]

	# no need after clean
	'''remove punctuation, lowercase, stem'''
	def normalize(self, text):
		return self.stem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punctuation_map)))

	def cosine_sim(self):
		return ((self.tfidf * self.tfidf.T).A)

	def euclidean_distance(self):
		return euclidean_distances(self.tfidf)

	def manhattan_distance(self):
		return manhattan_distances(self.tfidf)


def calculate_similarity(documents):
	sim = Similarity(documents)
	sim.word2vec()
	print 'Cosine Similarity:'
	print sim.cosine_sim()
	print '-' * 50
	print 'Euclidean Distance:'
	print sim.euclidean_distance()
	print '-' * 50
	print 'Manhattan Distance:'
	print sim.manhattan_distance()


if __name__ == '__main__':
	files = ['test/transcript.txt', 'test/forum.txt', 'test/forum_diff.txt']
	documents = [open(f).read() for f in files]
	calculate_similarity(documents)
