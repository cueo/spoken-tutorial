from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = Word2Vec.load('snippet.model')
'''
print model.most_similar('array')
print model.most_similar('return')
'''

dimension = 8
snippet = 'Comments are used to understand the flow of program. It is useful for documentation. It gives us information about the program. The double slash is called as single line comment'.decode('utf-8')
snippet_vector = np.zeros((1, dimension))
for word in snippet:
	if word in model.vocab:
		vecvalue = model[word].reshape(1, dimension)
		snippet_vector = np.add(snippet_vector, vecvalue)

link_text = 'Im used to // to mark a single line comment from Java and Visual Studio and was surprised that this does not exist for Ansi-C. Using /* my comment */is quite annoying. Is there any other way to mark a single line comment when using Ansi-C?'.decode('utf-8')
link_vector = np.zeros((1, dimension))
for word in link_text:
	if word in model.vocab:
		vecvalue = model[word].reshape(1, dimension)
		link_vector = np.add(link_vector, vecvalue)
	
print link_vector.shape
print cosine_similarity(snippet_vector, link_vector)