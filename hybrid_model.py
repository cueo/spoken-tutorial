from hybrid import calculate_keyword_similarity
from hybrid import pairwise_word2vec


def hybrid_similarity(script, forum):
	"""
	Hybrid approach:
		1) Compute keyword cosine, if < low -> IR
		2) Else, compute word2vec, if > high -> R
		3) Else, SR
	"""

	# comparison param
	high = 0.5
	low = 0.1

	sentences = [script, ' '.join(forum)]

	similarity = calculate_keyword_similarity(sentences)

	if similarity < low:
		relevance = 'IR'
	else:
		# max word2vec
		similarity = pairwise_word2vec(script, forum)[1]
		if similarity > high:
			relevance = 'R'
		else:
			relevance = 'SR'

	return relevance, similarity
