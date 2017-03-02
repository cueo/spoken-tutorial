from nltk import *
from gensim.models import Word2Vec

import logging
import numpy as np
import pickle

def process(forum_data):
	text = []
	for entry in forum_data:
		values = forum_data[entry] #[question,answer1,answer2...]
		for i in values:
			values1 = [j for j in i.split()]
			text.append(values1)
		vectors  = word2vecmodel(text)
		Xforum_data[entry] = vectors

def processSnippet(snippets):
	text = [] #["snippet 1","snippet 2",...]
	for entry in snippets:
		values = [i for i in entry.split()]
		text.append(values)
	vectors = word2vecmodel(text)
	fp = open('Word2vec_snippets','wb')
	pickle.dump(vectors,fp)


def word2vecmodel(text):
	Xtext = np.zeros((len(text), 16))
	vecvalue = np.zeros((1,16))
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	model = Word2Vec(text, size=16, min_count=1)
	model_name = "text.bin"
	model.save(model_name)
	model = Word2Vec.load(model_name)

	i = 0

	for sentence in text:
		vector = np.zeros((1,16))
		for word in sentence:
			vecvalue = model[word].reshape(1,16)
			vector= np.add(vector, vecvalue)
		Xtext[i] = vector
		i = i + 1

	return Xtext



if __name__ == '__main__':
	Xforum_data = {}
	fp = open('data/data.pkl','r')
	forum_data = pickle.load(fp)
	#print forum_data
	process(forum_data)
	#print Xforum_data
	fp = open('Word2vec_forum.','wb')
	pickle.dump(Xforum_data,fp)
	



	

