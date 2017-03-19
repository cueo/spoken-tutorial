from numpy import dot
from numpy.linalg import norm
from preprocess import simple_clean
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from stack import get_answers

import itertools
import re


def remove_duplicates(text):
	text = re.sub('\d+'," ",text)
	return ' '.join(set(text.split()))


def tf_matrix(documents):
	tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0)
	tfidf_matrix = tf.fit_transform(documents)
	# feature_names = tf.get_feature_names()
	# print feature_names
	return tfidf_matrix


def svd(matrix):
	svd = TruncatedSVD(100)
	lsa = make_pipeline(svd, Normalizer(copy=False))
	matrix = lsa.fit_transform(matrix)
	return matrix


def cosine(vector1, vector2):
	return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))


def lsa_similarity(documents):
	tfidf_matrix = tf_matrix(documents)
	lsa = svd(tfidf_matrix)
	# print lsa

	values = list(itertools.combinations(lsa, 2))
	sim = 0
	for i in values:
		sim += cosine(i[0], i[1])

	return sim


if __name__ == "__main__":
	documents = []
	transcript_path = 'data/C and Cpp/Working-With-Structures.txt'
	with open(transcript_path, 'r') as f:
		file = f.read()
	transcript = simple_clean(file)
	transcript = re.sub('\d+', ' ', transcript)
	documents.append(transcript)
	
	forum_id = 26188265 	# R
	# forum_id = 17250480  	# SR
	# forum_id = 9593798  	# IR

	question, answers = get_answers(forum_id)
	# an i for an i will make the whole world blind
	answers = ' '.join(i for i in answers)
	documents.append(answers)

	similarity = lsa_similarity(documents)
	print(similarity)
