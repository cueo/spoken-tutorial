import pickle
import lxml.html
import re
import os

def retrieve_title(qid):
	url = 'http://stackoverflow.com/questions/' + qid
	data = lxml.html.parse(url)
	title = data.find('.//title').text
	title = re.search(r'(.*)? - Stack Overflow', title).group(1)
	# return data.find('.//title').text
	return title

if __name__ == '__main__':
	with open('data.pkl', 'rb') as f:
		stack_data = pickle.load(f)
	title_dict = {}
	if os.path.exists('title.pkl'):
		with open('title.pkl', 'rb') as f:
			title_dict = pickle.load(f)
	retrieved_keys = title_dict.keys()
	for qid in stack_data.keys():
		if qid not in retrieved_keys:
			try:
				title = retrieve_title(qid)
				print(qid, ':', title)
				title_dict[qid] = title
			except Exception as e:
				print('Exception: ', e)
				print("Couldn't fetch:", qid)
				title_dict[qid] = qid
		else:
			print('Already fetched qid:', qid)
	with open('title.pkl', 'wb') as f:
		pickle.dump(title_dict, f)
