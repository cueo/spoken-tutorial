import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation + '“”')

def stem_tokens(tokens):
	return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
	return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(files):
	documents = [open(f).read() for f in files]
	tfidf = vectorizer.fit_transform(documents)
	return ((tfidf * tfidf.T).A)

if __name__ == '__main__':
	files = ['test/transcript.txt', 'test/forum.txt', 'test/forum_diff.txt']
	sim = cosine_sim(files)
	print(sim)