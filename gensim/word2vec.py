import os
import re
import time
from gensim.models import Word2Vec
from nltk.corpus import stopwords


class DirectoryReader(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for file_name in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, file_name), encoding='utf-8'):
                line = preprocess(line)
                if len(line) > 2:
                    yield line


def preprocess(line: str):

    # ELiminar caracteres que no sean del alfabeto o espacios
    line = re.sub(r'[^a-zA-ZÀ-ÿ\u00f1\u00d1 ]', '', line)

    stoplist = stopwords.words('spanish') + 'así cada demás mediante ningún si tal'.split()

    return [token for token in line.lower().split() if token not in stoplist and len(token) > 1]



corpus = DirectoryReader(dirname="corpus")

control = time.time()
print('Preparing your model...')

model = Word2Vec(sentences=corpus, vector_size=300,
                 window=5, min_count=1, workers=4)
model.wv.save("word2vec.wordvectors")
print(f'Time taken : {(time.time() - control) / 60:.2f} mins\n')

print(model.wv.most_similar(positive=['gobierno']))
