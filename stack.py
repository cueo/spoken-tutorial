import stackexchange
from html2text import html2text
from preprocess import simple_clean as clean

so = stackexchange.Site(stackexchange.StackOverflow)
so.be_inclusive()


def get_answers(qid):
	question = so.question(qid)
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
