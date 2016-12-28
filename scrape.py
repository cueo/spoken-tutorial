# from lxml import html
# import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re

url = 'http://spoken-tutorial.org/tutorial-search/'
course = ''

def get_courses():
	print('Looking up:', url)
	page = urlopen(url)
	'''
	# Avoid downloading the page again and again
	search_file = 'search.html'
	if os.path.exists(search_file):
		with open(search_file, 'rb') as f:
			page = urlopen(os.path.join(os.getcwd(), search_file))
	else:
		page = urlopen(url)
		page_content = page.read()
		with open(search_file, 'wb') as f:
			f.write(page_content)
	'''
	soup = BeautifulSoup(page, 'lxml')
	'''
	# It is the first select tag that contains all the courses.
	# We extract the option tags for which it is a parent.
	'''
	courses = []
	select = soup.find_all('select')[0]
	options = select.find_all('option')
	for option in options:
		value = option['value']
		if 'Libre' in value:
			courses.append(value)
	return courses

def get_tutorials(course, language):
	course_url = 'http://spoken-tutorial.org/tutorial-search/?search_foss=' + course.replace(' ', '+') + '&search_language=' + language
	print('Querying:', course_url)
	page = urlopen(course_url)
	soup = BeautifulSoup(page, 'lxml')
	'''
	# Extract the names of the tutorials available for the queried course.
	# Note: the tutorials might span more than one page.
	# Also, search might return 0 results.
	# Need to handle these, not doing it right now.
	'''
	tutorials = []
	# Get the divs which contain the required results
	results = soup.find_all('div', {'class': 'result-record'})
	for div in results:
		tutorials.append('http://spoken-tutorial.org/' + div.a['href'])
	return tutorials

def get_scripts(tutorial):
	print('Downloading script for tutorial:', tutorial)
	page = urlopen(tutorial)
	soup = BeautifulSoup(page, 'lxml')
	# Get the link for the timed script.
	divs = soup.find_all('div', {'class': 'list-group-item-container'})
	script_url = 'empty'
	for div in divs:
		if div.h4.text[1] == 'T':
			script_url = div.a['href']
			break
	'''
	# Save the content of the timed script to a file.
	# The source has some keywords in bold, which is not reflected here.
	# Figure out a way around this.
	'''
	page = urlopen(script_url)
	soup = BeautifulSoup(page, 'lxml')
	title = str(soup.title).split('/')[2]
	directory = os.path.join('Scripts', course)
	if not os.path.exists(directory):
		os.mkdir(directory)
	file = os.path.join(directory, title + '.txt')
	print('\tWriting to file:', file)
	if not os.path.exists(file):
		content = soup.table.text
		content = re.sub('\n\n', '\n', content)
		with open(file, 'w', encoding='utf-8') as f:
			f.write(content[content.index('0'):])

if __name__ == '__main__':
	courses = get_courses()
	languages = ['English']
	for _course in courses:
		course = _course
		tutorials = get_tutorials(course, languages[0])
		for tutorial in tutorials:
			script = get_scripts(tutorial)