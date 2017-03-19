from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re
import json
from data import urls

'''
Format of the json
{
	"posts": [{
		"question": {
			"question": "text",
			"id": "1"
		},
		"answers": [{
			"answer": "text",
			"is_accepted": "true",
			"score": "3"
		}, {
			"answer": "text",
			"is_accepted": "false",
			"score": "3"
		}]
	}, {
		"question": {
			"question": "text",
			"id": "5898"
		},
		"answers": [{
			"answer": "text",
			"is_accepted": "true",
			"score": "0"
		}]
	}]
}
'''

def get_posts():
	print('Retrieving question...')
	question_div = soup.find('div', class_='js-question')
	question_text = question_div.find('div', class_='js-editable-content').text
	
	answers = []
	answer_divs = soup.find_all('div', class_='answer')
	for answer_div in answer_divs:
		print('\tRetrieving answer...')
		answer_text = answer_div.find('div', class_='js-editable-content').text
		score = answer_div.find('div', class_='vote-number').text
		is_accepted = 'false'
		if 'accepted-answer' in answer_div['class']:
			is_accepted = 'true'
		answer = {'answer': answer_text, 'score': score, 'is_accepted': is_accepted}
		answers.append(answer)
	
	question = {'question': question_text, 'id': question_id}
	posts = {'question': question, 'answers': answers}
	
	return posts

if __name__ == '__main__':
	items = []
	urls = urls[:3]
	for url in urls:
		print('\nLooking up:', url)
		question_id = url.split('/')[5]
		page = 	urlopen(url)
		soup = BeautifulSoup(page, 'lxml')
		posts = get_posts()
		items.append(posts)

	post_json = json.dumps({'posts': items}, indent=4)
	print(post_json)