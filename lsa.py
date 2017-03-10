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
import scipy as sc

def remove_duplicates(text):
	text = re.sub('\d+'," ",text)
	return ' '.join(set(text.split()))

def tf_matrix(documents):
	tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0)
	tfidf_matrix =  tf.fit_transform(documents)
	feature_names = tf.get_feature_names() 
	return tfidf_matrix
	#print feature_names

def svd(matrix):
	svd = TruncatedSVD(100)
	lsa = make_pipeline(svd, Normalizer(copy=False))
	matrix = lsa.fit_transform(matrix)
	return matrix

def cosine(vector1,vector2):	
	return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))

if __name__ == "__main__":
	documents = []
	transcript_path = 'data/C and Cpp/Working-With-Structures.txt'
	f = open(transcript_path)
	file = f.read()
	transcript = simple_clean(file)
	transcript = re.sub('\d+'," ",transcript)
	documents.append(transcript)
	
	#http://stackoverflow.com/questions/26188265/c-declare-the-struct-before-definition R
	#http://stackoverflow.com/questions/17250480/c-declaring-int-array-inside-struct SR
	forum_id = 9593798 #IR
	question,answers = get_answers(forum_id)
	answers = ' '.join(i for i in answers)
	documents.append(answers)
	tfidf_matrix = tf_matrix(documents)
	lsa = svd(tfidf_matrix)

	print lsa
	
	values = list(itertools.combinations(lsa,2))
	sim = 0

	for i in values:
		sim = sim + cosine(i[0],i[1])

	print sim
	

