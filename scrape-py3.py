# from lxml import html
# import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import re 

url = 'http://spoken-tutorial.org/tutorial-search/'
course = ''
# R => maximum number of results per page + 1
R = 21


def get_courses():
	print(('Looking up:', url))
	page = urlopen(url)
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
		text = option.text
		# courses = LibreOffice
		'''
		if 'Libre' in value:
			courses.append(value)
		'''
		search_courses = ['Advance C', 'C and Cpp', 'BASH']
		# condition = (value == 'Advance C' or value == 'BASH' or value == 'C and Cpp')
		if value in search_courses:
			courses.append(text)
	print(courses)
	return courses


def get_tutorials(course, pages, language):
	course_url = 'http://spoken-tutorial.org/tutorial-search/?search_foss=' + course.replace(' ', '+') + '&search_language=' + language
	'''
	# Extract the names of the tutorials available for the queried course.
	# Note: the tutorials might span more than one page.
	# Also, search might return 0 results.
	# Need to handle these, not doing it right now.
	'''
	tutorials = []
	for p in range(pages):
		new_url = course_url + '&page=' + str(p+1)
		print(('Querying:', new_url))
		page = urlopen(new_url)
		soup = BeautifulSoup(page, 'lxml')
		# Get the divs which contain the required results
		results = soup.find_all('div', {'class': 'result-record'})
		for div in results:
			tutorials.append('http://spoken-tutorial.org' + div.a['href'])
	return tutorials


def get_scripts(tutorial):
	print(('Downloading script for tutorial:', tutorial))
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
	directory = os.path.join('scripts', course)
	if not os.path.exists(directory):
		os.makedirs(directory)
	file = os.path.join(directory, title + '.txt')
	print(('\tWriting to file:', file))
	if not os.path.exists(file):
		content = soup.table.text
		content = re.sub('\n\n', '\n', content)
		with open(file, 'w', encoding='utf-8') as f:
			f.write(content[content.index('0'):])


if __name__ == '__main__':
	courses = get_courses()
	languages = ['English']
	for course_ in courses:
		re_match = re.search('(.*) \((\d+)\)', course_)
		course = re_match.group(1)
		pages = int(re_match.group(2)) // R + 1
		tutorials = get_tutorials(course, pages, languages[0])
		for tutorial in tutorials:
			script = get_scripts(tutorial)
