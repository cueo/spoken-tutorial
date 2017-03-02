import stackexchange
from html2text import html2text
from preprocess import simple_clean as clean


def get_answers(qid, site='stackoverflow.com'):
	if site.startswith('stacko'):
		# StackOverflow
		se = stackexchange.Site(stackexchange.StackOverflow)
	elif site.startswith('unix'):
		# Unix StackExchange
		se = stackexchange.Site(stackexchange.UnixampLinux)
	elif site.startswith('sup'):
		# Supa Hot Fire
		se = stackexchange.Site(stackexchange.SuperUser)
	elif site.startswith('ser'):
		# ServerFault
		se = stackexchange.Site(stackexchange.ServerFault)
	else:
		pass

	se.be_inclusive()

	question = se.question(qid)
	question_text = clean(question.title) + ' ' + clean(html2text(question.body))
	answers = []
	for answer in question.answers:
		answers.append(clean(html2text(answer.body)))
	return question_text, answers


if __name__ == '__main__':
	qid = '571076'
	question, answers = get_answers(qid)
	print question
	print answers
