from os import listdir
from os.path import isfile, join
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence

class LabeledLineSentence(object):
	def __init__(self, data):
		self.data = data
	def __iter__(self):
		for idx, doc in enumerate(self.data):
			yield LabeledSentence(doc.split(), 'SENT_%s' % idx)

if __name__ == "__main__":
	data_dir_paths = ['C and Cpp', 'BASH', 'Advance C']
	docLabels = [[i+'/'+f for f in listdir(i)] for i in data_dir_paths]
	docLabels = [item for sublist in docLabels for item in sublist]
	#print docLabels

	data = []
	for doc in docLabels:
		data.append(open(doc).read().strip())
	
	#it = DocIt.DocIterator(data, docLabels)
	sentences = LabeledLineSentence(data)
	model = Doc2Vec(size=300, window=10, min_count=5, workers=11, alpha=0.025, min_alpha=0.025) # train_lbls=False use fixed learning rate
	model.build_vocab(sentences)
	for epoch in range(10):
		model.train(sentences)
		model.alpha -= 0.002 # decrease the learning rate
		model.min_alpha = model.alpha # fix the learning rate, no deca
		model.train(sentences)

model.save('Doc2Vec.model')
print(model.most_similar('array'))