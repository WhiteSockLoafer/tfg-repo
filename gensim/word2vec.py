import os
import re
import time
from gensim.models import Word2Vec


def preprocessing(file: str):

    if not os.path.isfile(file):
        print('File not found')
        return

    try:
        f = open(file)
    except IOError:
        print('File not accesible')
        return

    content = f.read()
    content = re.sub(r'\,', '', content)
    content = re.sub(r'[^a-zA-ZÀ-ÿ\u00f1\u00d1\n ]', '\n', content)
    content = re.sub(r'^ +| +$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n{2,}', '\n', content)
    content = content.split('\n')

    phrases: list[str] = []
    for line in content:
        if len(line.split()) > 2:
            phrases.append(line.lower().split())

    return phrases


control = time.time()
print('Preprocessing your corpus...')

phrases = preprocessing('corpus/constitucion')
print(f'Time taken : {(time.time() - control) / 60:.2f} mins\n')

control = time.time()
print('Preparing your model...')

model = Word2Vec(sentences=phrases, vector_size=100,
                 window=5, min_count=1, workers=4)
print(f'Time taken : {(time.time() - control) / 60:.2f} mins\n')

print(model.wv.most_similar('españa'))