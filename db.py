import sqlite3
import os
import pickle

from window import calculate_interval
from hybrid_model import hybrid_similarity

LINKS = 10


def push(stack, qid, relevance, similarity):
	l = len(stack)
	if stack and l < LINKS:
		if similarity > stack[-1][1]:
			for i in range(l):
				entry = stack[i]
				entry_sim = entry[2]
				if similarity > entry_sim:
					stack.insert(i, (qid, relevance, similarity))
					break
	else:
		stack.append((qid, relevance, similarity))
	return stack[:10]


def populate_db(file, snippets, times):
	with open('../data/data.pkl', 'rb') as f:
		stack_data = pickle.load(f)
	with open('../data/title.pkl', 'rb') as f:
		title_data = pickle.load(f)
	for index in range(len(snippets)):
		snippet = snippets[index]
		for qid, forum in stack_data.items():
			relevance, similarity = hybrid_similarity(snippet, forum)
			relevant_link_stack = push(relevant_link_stack, qid, relevance, similarity)
		links = [i[0] for i in relevant_link_stack]
		relevance = [i[1] for i in relevant_link_stack]
		titles = [title_data[qid] for qid in links]

		conn.execute(
			'''INSERT INTO spoken_tutorial (file_name, time, links, relevance, titles) VALUES (?, ?, ?, ?, ?)''',
			(file, times[index], '::'.join(links), '::'.join(relevance), '::'.join(titles)))


def create_db(path):
	conn.execute('''CREATE TABLE IF NOT EXISTS spoken_tutorial
			(id INTEGER PRIMARY KEY AUTOINCREMENT,
			file_name TEXT NOT NULL,
			time INTEGER NOT NULL,
			links TEXT,
			relevance TEXT,
			titles TEXT);
			''')
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
				populate_db(f, snippets, times)
	conn.commit()
	conn.close()


if __name__ == '__main__':
	conn = sqlite3.connect('ui.db')
	print('Connected successfully!')
	path = '../data'
	create_db(path)
