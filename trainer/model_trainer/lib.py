import os
import re
import statistics
import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from gensim.models import Word2Vec, FastText


''' Lector de ficheros en texto plano de cierto directorio, 
    memory-friendly y preprocesado con preprocess()'''


class DirectoryCorpusReader(object):

    def __init__(self, dir_path):
        self.dir_path = dir_path

    def __iter__(self):
        for file_name in os.listdir(self.dir_path):
            for line in open(os.path.join(self.dir_path, file_name), encoding='utf-8'):
                line = self.preprocess(line)
                if len(line) > 2:  # Solo líneas mayores de 2 palabras
                    yield line

    def preprocess(self, line: str):
        # Eliminar caracteres que no sean del alfabeto castellano o espacios
        line = re.sub(r'[^a-zA-ZÀ-ÿ\u00f1\u00d1 ]', '', line)
        return [token for token in line.lower().split() if len(token) > 2]


class AnalogiesDatasetReader(object):

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def analogies(self):
        for line in open(self.dataset_path, encoding='utf-8'):
            yield line.split()
    
    def __len__(self) -> int:
        with open(self.dataset_path) as f:
            len = sum(1 for line in f)
        return len

    def evaluate(self, models_dir: str, topn: int) -> dict:
        results = []
        bad = [0 for i in range(len(self))]
        model_index = 0
        for file_name in os.listdir(models_dir):
            if file_name.endswith('.model'):
                model_index += 1
                if 'fasttext' in file_name:
                    model = FastText.load(os.path.join(models_dir, file_name))
                else:
                    model = Word2Vec.load(os.path.join(models_dir, file_name))

                marks = []

                for i, analogy in enumerate(self.analogies()):
                    try:
                        similars = model.wv.most_similar(
                            negative=[analogy[0]], positive=[analogy[1], analogy[2]], topn=topn)
                    except KeyError:
                        marks.append(topn)
                        bad[i] += 1
                    else:
                        similar = next(((index, tuple) for (index, tuple) in enumerate(similars) if tuple[0] == analogy[3]), None)
                        if similar is None:
                            marks.append(topn)
                            bad[i] += 1
                        else:
                            marks.append(similar[0])

                results.append(
                    {
                        "id": model_index,
                        "model_name": file_name,
                        "window": model.window,
                        "vector_size": model.vector_size,
                        "marks": marks,
                        "accuracy": 100 - (100/len(self) * sum(marks)/topn)
                    }
                )
        bads = [index + 1 for index, errors in enumerate(bad) if errors == model_index]
        return results, bads


def makeplots(report: dict):
    x = [model["id"] for model in report]
    y = [model["accuracy"] for model in report]

    plt.plot(x, y, marker=".")
    plt.xlabel("Model ID")
    plt.ylabel("Accuracy")
    return plt
