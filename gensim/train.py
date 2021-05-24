import os
import re
import time
from gensim.models import Word2Vec
from nltk.corpus import stopwords


# Lector de ficheros en texto plano de cierto directorio
class DirectoryReader(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for file_name in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, file_name), encoding='utf-8'):
                line = preprocess(line)
                if len(line) > 2: # Solo líneas mayores de 2 palabras
                    yield line


# Preprocesamiento de las lineas de los ficheros
def preprocess(line: str):

    # ELiminar caracteres que no sean del alfabeto o espacios
    line = re.sub(r'[^a-zA-ZÀ-ÿ\u00f1\u00d1 ]', '', line)

    # Palabras ruidosas para nuestro modelo
    stoplist = stopwords.words('spanish') + 'así cada demás mediante ningún tal ello puede ser pueda'.split()

    return [token for token in line.lower().split() if token not in stoplist and len(token) > 2]



corpus = DirectoryReader(dirname='corpus')

print('Preparing your model...')
control = time.time()


model = Word2Vec(sentences=corpus, vector_size=300,
                 window=5, min_count=10, workers=4)
print(f'Time taken : {(time.time() - control) / 60:.2f} mins\n')

model.save('modelo/boe.model')
model.wv.save('modelo/boe.wordvectors')
