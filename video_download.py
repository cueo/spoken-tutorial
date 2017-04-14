import os
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup

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


def get_videos(tutorial):
	page = urlopen(tutorial)
	soup = BeautifulSoup(page, 'lxml')
	video = soup.find(name='source')
	src = 'http://spoken-tutorial.org' + video['src']
	directory = tutorial.split('/')[-3].replace('+', ' ')
	video_file = urlopen(src)
	file_path = os.path.join(path, directory, src.split('/')[-1])
	if not os.path.exists(file_path):
		print('Downloading video for tutorial:', tutorial)
		with open(file_path, 'wb') as f:
			f.write(video_file.read())


if __name__ == '__main__':
	path = 'data/videos'
	if not os.path.exists(path):
		os.mkdir(path)
	courses = get_courses()
	languages = ['English']
	for course_ in courses:
		re_match = re.search('(.*) \((\d+)\)', course_)
		course = re_match.group(1)
		pages = int(re_match.group(2)) // R + 1
		tutorials = get_tutorials(course, pages, languages[0])
		for tutorial in tutorials:
			get_videos(tutorial)
