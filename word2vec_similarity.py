import numpy as np
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine


def avg_feature_vector(words, model, index2word_set, num_features=100):
	# function to average all words vectors in a given paragraph
	feature_vec = np.zeros((num_features,), dtype="float32")
	nwords = 0

	for word in words:
		if word in index2word_set:
			nwords += 1
			feature_vec = np.add(feature_vec, model[word])
	if nwords > 0:
		feature_vec = np.divide(feature_vec, nwords)
	return feature_vec


if __name__ == '__main__':
	snippet = 'comments c removed compiled comments c source file removed compiler example visual c gcc'
	forum = 'compiler uses different steps translate sourcecode machine readable code first step lexical analysis \
	phase translates characters tokens token identifier literal \
	value reserved word operator comments whitespace mostly ignored phase used separate \
	different tokens next steps concept comment whitespace yes removed compiling'

	model = Word2Vec.load('data/snippet.model')
	# list containing names of words in the vocabulary
	word_index_set = set(model.index2word)

	snippet_vector = avg_feature_vector(snippet.split(), model, word_index_set)
	forum_vector = avg_feature_vector(forum.split(), model, word_index_set)

	similarity = 1 - cosine(snippet_vector, forum_vector)
	print(similarity)
