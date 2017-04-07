import csv
import pickle
import numpy as np
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt
from random import choice

from preprocess import simple_clean
from window import get_pairwise_similarity
from lsa import lsa_similarity
from rake.rake import extract_keywords
from similarity import calculate_similarity
from word2vec_similarity import avg_feature_vector
from irrelevant_keys import ir_keys


def get_data(path, data_set='R'):
	scripts = []
	forums = []
	data_path = 'data/data.pkl'
	if data_set == 'IR':
		data_path = 'data/ir_data.pkl'
	with open(data_path, 'rb') as pklfile:
		forum_data = pickle.load(pklfile)

	with open(path, 'r', encoding='utf-8') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		for row in reader:
			script = row[2]
			link = row[3]
			relevance = row[4]
			if relevance == data_set:  # R, SR, IR
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
							if data_set == 'IR':
								qid = choice(ir_keys)
							forum = forum_data[qid]
							scripts.append(script)
							forums.append(forum)
						except Exception as e:
							print("Couldn't find qid:", qid)
							print('Reason:', e)

	return scripts, forums


def calculate_word2vec_similarity(sentences):
	model = Word2Vec.load('data/snippet.model')
	word_index_set = set(model.index2word)
	script_vector = avg_feature_vector(sentences[0].split(), model, word_index_set)
	forum_vector = avg_feature_vector(sentences[1].split(), model, word_index_set)
	word2vec_similarity = 1 - cosine(script_vector, forum_vector)
	return word2vec_similarity


if __name__ == '__main__':
	path = 'data/Links to topics v2.1 - Sheet1.csv'
	data_set = 'R'
	# get the transcript and the forum data
	scripts, forums = get_data(path, data_set)

	if data_set == 'R':
		similarity_range = (0.4, 1)
	elif data_set[0] == 'S':
		similarity_range = (0.2, 0.4)
	else:
		similarity_range = (-1, 0.2)

	l = len(scripts)
	evaluated_scripts = 0

	sum_sim, sub_sim, max_sim, min_sim = [], [], [], []
	lsa_sim = []
	key_cosine_sim, key_word2vec_sim = [], []
	word2vec_sim = []

	for index in range(l):
		print('Evaluating: %d/%d' % (index+1, l))
		script = scripts[index]
		forum = forums[index]

		# clean script
		script = simple_clean(script)

		# compare using cosine similarity
		try:
			similarity = get_pairwise_similarity(script, forum)
			evaluated_scripts += 1
		except Exception as e:
			print('Exception:', e)
			print('Script:', script)
			print('Forum:', forum)
		sum_sim.append(similarity[0])
		# sub_sim.append(similarity[1])
		max_sim.append(similarity[2])
		# min_sim.append(similarity[3])

		# LSA
		sentences = [script, ' '.join(forum)]
		try:
			lsa_sim.append(lsa_similarity(sentences))
		except ValueError:
			lsa_sim.append(0)

		# keyword matching
		script_keywords = extract_keywords(sentences[0])
		if not script_keywords:
			script_keywords = sentences[0]
		forum_keywords = extract_keywords(sentences[1])
		if not forum_keywords:
			forum_keywords = sentences[1]
		sk = ' '.join([x[0] for x in script_keywords])
		fk = ' '.join([x[0] for x in forum_keywords])
		documents = [sk, fk]
		keyword_word2vec = calculate_word2vec_similarity(documents)  # using word2vec
		try:
			keyword_cosine = calculate_similarity(documents)[0][1]  # using cosine
		except RuntimeError:
			keyword_cosine = 0
		key_word2vec_sim.append(keyword_word2vec)
		key_cosine_sim.append(keyword_cosine)

		# word2vec similarity
		word2vec_similarity = calculate_word2vec_similarity(sentences)
		word2vec_sim.append(word2vec_similarity)

	x = np.arange(l)

	print('=' * 50)
	print('{:30}{}'.format('Sum cosine similarities:', sum_sim))
	print('{:30}{}'.format('Max cosine similarities:', max_sim))
	print('{:30}{}'.format('LSA similarities:', lsa_sim))
	print('{:30}{}'.format('Keyword cosine similarities:', key_cosine_sim))
	print('{:30}{}'.format('Keyword word2vec similarities:', key_word2vec_sim))
	print('{:30}{}'.format('Word2Vec similarities:', word2vec_sim))
	print('=' * 50)

	# plot
	plt.figure(1)
	red_dot, = plt.plot(x, sum_sim, 'ro', color='red')
	blue_dot, = plt.plot(x, max_sim, 'ro', color='blue')
	green_dot, = plt.plot(x, lsa_sim, 'ro', color='green')
	orange_dot, = plt.plot(x, key_cosine_sim, 'ro', color='orange')
	cyan_dot, = plt.plot(x, key_word2vec_sim, 'ro', color='cyan')
	magenta_dot, = plt.plot(x, word2vec_sim, 'ro', color='magenta')

	plt.legend([red_dot, blue_dot, green_dot, orange_dot, cyan_dot, magenta_dot], ['cosine sum', 'cosine max', 'lsa', 'keyword cosine', 'keyword word2vec' 'word2vec similarity'])
	plt.show()

	n = np.arange(3)
	ss_accuracy, ms_accuracy, lsa_accuracy, key_cosine_accuracy, key_word2vec_accuracy, word2vec_accuracy = 0, 0, 0, 0, 0, 0
	for i in range(l):
		ss, ms, lsa, kcs, kws, ws = sum_sim[i], max_sim[i], lsa_sim[i], key_cosine_sim[i], key_word2vec_sim[i], word2vec_sim[i]
		if similarity_range[0] < ss <= similarity_range[1]:
			ss_accuracy += 1
		if similarity_range[0] < ms <= similarity_range[1]:
			ms_accuracy += 1
		if similarity_range[0] < lsa <= similarity_range[1]:
			lsa_accuracy += 1
		if similarity_range[0] < kcs <= similarity_range[1]:
			key_cosine_accuracy += 1
		if similarity_range[0] < kws <= similarity_range[1]:
			key_word2vec_accuracy += 1
		if similarity_range[0] < ws <= similarity_range[1]:
			word2vec_accuracy += 1

	ss_accuracy /= evaluated_scripts
	ms_accuracy /= evaluated_scripts
	lsa_accuracy /= evaluated_scripts
	key_cosine_accuracy /= evaluated_scripts
	key_word2vec_accuracy /= evaluated_scripts
	word2vec_accuracy /= evaluated_scripts

	y = np.array([ss_accuracy, ms_accuracy, lsa_accuracy, key_cosine_accuracy, key_word2vec_accuracy, word2vec_accuracy])
	x = np.arange(len(y))
	c = ['r', 'b', 'g', 'orange', 'c', 'm']
	area = np.pi * (50 * y) ** 2

	print('Evaluated scripts: %d/%d' % (evaluated_scripts, l))
	print('=' * 50)
	print('{:28}{}'.format('Sum cosine accuracy:', ss_accuracy))
	print('{:28}{}'.format('Max cosine accuracy:', ms_accuracy))
	print('{:28}{}'.format('LSA accuracy:', lsa_accuracy))
	print('{:28}{}'.format('Keyword cosine accuracy:', key_cosine_accuracy))
	print('{:28}{}'.format('Keyword word2vec accuracy:', key_word2vec_accuracy))
	print('{:28}{}'.format('Word2Vec accuracy:', word2vec_accuracy))
	print('=' * 50)

	# accuracy plot
	plt.figure(2)
	plt.scatter(x, y, s=area, c=c, alpha=0.7)
	plt.ylabel('accuracy')
	plt.show()
	plt.close()
