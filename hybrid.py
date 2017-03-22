import csv
import pickle

from similarity import calculate_similarity
from rake.rake import extract_keywords
from benchmarks import calculate_word2vec_similarity
from window import get_pairwise_similarity


def get_data(path):
	pklpath = 'data/data.pkl'
	with open(pklpath, 'rb') as f:
		forum_data = pickle.load(f)

	with open(path, 'r', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		scripts, forums, dataset = [], [], []
		for row in reader:
			script = row[2]
			link = row[3]
			relevance = row[4]
			# check if scripts are empty (because incomplete data)
			if script:
				# if a script has more than one matching forums, taking just the first one
				if '\n' in link:
					link = link.split('\n')[0]
				details = link.split('/')
				# check if the links are proper (because discrepancies in data)
				if len(details) > 5:
					qid = details[-2]
					try:
						forum = forum_data[qid]
						scripts.append(script)
						forums.append(forum)
						dataset.append(relevance)
					except Exception as e:
						print("Couldn't find qid:", qid)
						print('Reason:', e)
		return scripts, forums, dataset


def calculate_keyword_similarity(sentences):
	script_keywords = extract_keywords(sentences[0])
	forum_keywords = extract_keywords(sentences[1])
	try:
		sk = ' '.join([x[0] for x in script_keywords])
		fk = ' '.join([x[0] for x in forum_keywords])
		documents = [sk, fk]
		similarity = calculate_similarity(documents)[0][1]  # using cosine
		# similarity = calculate_word2vec_similarity(documents)  # using word2vec
	except TypeError:
		print('Error: no matching keywords!')
		similarity = 0
	return similarity


def approach_one():
	"""
	Hybrid approach:
		1) Compute the keyword-based cosine similarity
		2) If it is "high" (relevant), use word2vec
		3) If it is "low" (irrelevant), use keyword-based cosine itself
		4) Otherwise, (slightly relevant) use max-cosine
	"""

	# comparison param
	high = 0.3
	low = 0.15

	hits = 0
	for i in range(l):
		print('%d/%d:' % (i, l), end=' ')
		script, forum, relevance = scripts[i], forums[i], dataset[i]
		sentences = [script, ' '.join(forum)]

		# Step 1: keyword matching (cosine)
		similarity = calculate_keyword_similarity(sentences)

		# Step 2: high -> word2vec
		if similarity > high:
			word2vec_similarity = calculate_word2vec_similarity(sentences)
			if word2vec_similarity >= high:
				predicted_relevance = 'R'
			elif word2vec_similarity <= low:
				predicted_relevance = 'IR'
			else:
				predicted_relevance = 'SR'

		# Step 3: low -> irrelevant
		elif similarity < low:
			predicted_relevance = 'IR'

		# Step 4: slightly relevant -> max cosine
		else:
			cosine_similarity = get_pairwise_similarity(script, forum)
			max_cosine = cosine_similarity[2]
			if max_cosine >= high:
				predicted_relevance = 'R'
			elif max_cosine <= low:
				predicted_relevance = 'IR'
			else:
				predicted_relevance = 'SR'

		print('Actual: %s\tPredicted: %s' % (relevance, predicted_relevance))
		if predicted_relevance == relevance:
			hits += 1

	print('Accuracy:', hits * 100 / l)


def approach_two():
	"""
	Hybrid approach:
		1) Compute keyword cosine, if it is < low, irrelevant
		2) Compute the word2vec similarity
		3) If it is "high" (relevant), it can be R or SR
			- Compute max cosine and see if it lies between (low, high) -> slightly relevant
			- Else, relevant
	"""

	# comparison param
	high = 0.5
	low = 0.2

	hits = 0
	for i in range(l):
		print('%d/%d:' % (i, l), end=' ')
		script, forum, relevance = scripts[i], forums[i], dataset[i]
		sentences = [script, ' '.join(forum)]

		# Step 1: keyword matching (cosine)
		similarity = calculate_keyword_similarity(sentences)
		if similarity < low:
			predicted_relevance = 'IR'
		else:
			similarity = calculate_word2vec_similarity(sentences)
			if similarity > high:
				# Step 3: compute max cosine
				cosine_similarity = get_pairwise_similarity(script, forum)
				max_cosine = cosine_similarity[2]
				if max_cosine < high:
					predicted_relevance = 'SR'
				else:
					predicted_relevance = 'R'
			else:
				predicted_relevance = 'SR'

		if predicted_relevance == relevance:
			hits += 1

		print('Actual: %s\tPredicted: %s' % (relevance, predicted_relevance))

	print('Accuracy:', hits * 100 / l)


def approach_three():
	"""
	Hybrid approach:
		1) Compute keyword cosine, if < low -> IR
		2) Else, compute word2vec, if > high -> R
		3) Else, SR
	"""

	# comparison param
	high = 0.65
	low = 0.1

	hits = 0
	for i in range(l):
		print('%d/%d:' % (i, l), end=' ')
		script, forum, relevance = scripts[i], forums[i], dataset[i]
		sentences = [script, ' '.join(forum)]

		# Step 1: keyword matching (cosine)
		similarity = calculate_keyword_similarity(sentences)
		if similarity < low:
			predicted_relevance = 'IR'
		else:
			similarity = calculate_word2vec_similarity(sentences)
			if similarity > high:
				predicted_relevance = 'R'
			else:
				predicted_relevance = 'SR'

		if predicted_relevance == relevance:
			hits += 1

		print('Actual: %s\tPredicted: %s' % (relevance, predicted_relevance))

	print('Accuracy:', hits * 100 / l)


def approach_four():
	"""
	plain word2vec
	"""

	# comparison param
	high = 0.5
	low = 0.3

	hits = 0
	for i in range(l):
		print('%d/%d:' % (i, l), end=' ')
		script, forum, relevance = scripts[i], forums[i], dataset[i]
		sentences = [script, ' '.join(forum)]

		# Step 1: keyword matching (cosine)
		similarity = calculate_word2vec_similarity(sentences)

		if similarity > high:
			predicted_relevance = 'R'
		elif similarity < low:
			predicted_relevance = 'IR'
		else:
			predicted_relevance = 'SR'

		if predicted_relevance == relevance:
			hits += 1

		print('Actual: %s\tPredicted: %s' % (relevance, predicted_relevance))

	print('Accuracy:', hits * 100 / l)


if __name__ == '__main__':
	path = 'data/Links to topics v2.1 - Sheet1.csv'
	# get the transcript and the forum data
	scripts, forums, dataset = get_data(path)
	l = len(dataset)
	print('=' * 50)
	print('Approach 1:')
	print('-' * 50)
	approach_one()
	print('=' * 50)
	print('Approach 2:')
	print('-' * 50)
	approach_two()
	print('=' * 50)
	print('=' * 50)
	print('Approach 3:')
	print('-' * 50)
	approach_three()
	print('=' * 50)
	print('=' * 50)
	print('Approach 4:')
	print('-' * 50)
	approach_four()
	print('=' * 50)
