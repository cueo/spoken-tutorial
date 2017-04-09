import sqlite3
import os
import pickle
import sys
from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
from window import calculate_interval
from stack import get_answers
from word2vec_similarity import avg_feature_vector

def populate_db(snippets, times, file_name):
	qids = []
	stack_data = None
	if os.path.exists('data/data.pkl'):
		with open('data/data.pkl', 'rb') as f:
			stack_data = pickle.load(f)
			qids = list(stack_data.keys())
	forum_texts = []
	for id_ in qids:
		forum_texts.append(stack_data[id_])
	#print(len(forum_texts[0]), forum_texts[0])

	#word2vec
	model = Word2Vec.load('data/snippet.model')
	word_index_set = set(model.wv.index2word)
	for i in range(len(snippets)):
		time = int(times[i].split(':')[0]) * 60 + int(times[i].split(':')[1])  #converting to seconds
		relevant_links, relevant_data = [-1, -1, -1], [(), (), ()]
		slightly_relevant_data = [('', '', sys.maxsize)]
		irrelevant_data = [('', '', sys.maxsize)]
		script_vector = avg_feature_vector(snippets[i].split(), model, word_index_set)
		print('Retrieving links for snippet', (i+1))
		for id_, QAs in stack_data.items():
			for forum_text in QAs:
				forum_vector = avg_feature_vector(forum_text.split(), model, word_index_set)
				word2vec_similarity = 1 - cosine(script_vector, forum_vector)
				if abs(word2vec_similarity) > 0.4 and abs(word2vec_similarity) > min(relevant_links):
					min_index = relevant_links.index(min(relevant_links))
					relevant_links[min_index] = abs(word2vec_similarity)
					relevant_data[min_index] = (forum_text, id_, abs(word2vec_similarity), 'Relevant')
				elif abs(word2vec_similarity) <= 0.4 and abs(word2vec_similarity) > 0.2 and abs(word2vec_similarity) < slightly_relevant_data[0][2]:
					slightly_relevant_data[0] = (forum_text, id_, abs(word2vec_similarity), 'Slightly relevant')
				elif abs(word2vec_similarity) <= 0.2 and abs(word2vec_similarity) < irrelevant_data[0][2]:
					irrelevant_data[0] = (forum_text, id_, abs(word2vec_similarity), 'Irrelevant')
		try:
			conn.executemany("INSERT INTO SPOKEN_TUTORIAL (FILE_NAME, TIME, SNIPPET_TEXT, FORUM_TEXT, LINK, SIMILARITY, RELEVANCE) VALUES (?, ?, ?, ?, ?, ?, ?);", list((file_name, time, snippets[i]) + data for data in relevant_data))
		except Exception as e:
			print(e, '------------>', 'Could not find relevant data')
		try:
			conn.executemany("INSERT INTO SPOKEN_TUTORIAL (FILE_NAME, TIME, SNIPPET_TEXT, FORUM_TEXT, LINK, SIMILARITY, RELEVANCE) VALUES (?, ?, ?, ?, ?, ?, ?);", list((file_name, time, snippets[i]) + data for data in slightly_relevant_data))
		except Exception as e:
			print(e, '------------>', 'Could not find slightly relevant data')
		try:
			conn.executemany("INSERT INTO SPOKEN_TUTORIAL (FILE_NAME, TIME, SNIPPET_TEXT, FORUM_TEXT, LINK, SIMILARITY, RELEVANCE) VALUES (?, ?, ?, ?, ?, ?, ?);", list((file_name, time, snippets[i]) + data for data in irrelevant_data))
		except Exception as e:
			print(e, '------------>', 'Could not find irrelevant data')
		#exit()
	
def create_db(path):
	conn.execute("""CREATE TABLE IF NOT EXISTS SPOKEN_TUTORIAL
	       (ID INTEGER PRIMARY KEY AUTOINCREMENT,
	       FILE_NAME TEXT NOT NULL,
	       TIME INTEGER NOT NULL,
	       SNIPPET_TEXT TEXT NOT NULL,
	       FORUM_TEXT TEXT,
	       LINK TEXT,
	       RELEVANCE TEXT,
	       SIMILARITY REAL);
	       """)
	print('Table created successfully!')

	for r, d, files in os.walk(path):
		for f in files:
			if f.endswith('.txt'):
				file_path = os.path.join(r, f)
				script, time_intervals, times = calculate_interval(file_path)
				snippets = []
				for t in range(len(time_intervals)):
					snippet = ' '.join(script[t:time_intervals[t]])
					snippets.append(snippet)
				print('Retrieving results for', f, '----------------->')
				populate_db(snippets, times, f)
	conn.commit()
	conn.close()

if __name__ == '__main__':
	conn = sqlite3.connect('test.db')
	print('Connected successfully!')
	create_db('data')