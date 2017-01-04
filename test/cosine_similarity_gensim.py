import nltk, string
from gensim import corpora, models, similarities
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
stop_words.extend([])

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation + '“”')

def stem_tokens(tokens):
	return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
	# return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
	words = nltk.word_tokenize(text.lower().translate(remove_punctuation_map))
	words = [word for word in words if word not in stop_words]
	return words

if __name__ == '__main__':
	files = ['test/transcript.txt', 'test/forum.txt']
	documents = [normalize(open(f).read()) for f in files]

	# create a dictionary of unique words
	dictionary = corpora.Dictionary(documents)

	# compile corpus (vectors number of times each elements appears)
	corpus = [dictionary.doc2bow(d) for d in documents]
	
	# transform text with tf-idf
	tfidf = models.TfidfModel(corpus)

	# corpus tf-idf
	corpus_tfidf = tfidf[corpus]

	# create a similarity matrix
	index = similarities.MatrixSimilarity(tfidf[corpus])

	sims = index[corpus_tfidf]
	print(sims)