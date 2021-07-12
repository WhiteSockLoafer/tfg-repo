import os
import re
import statistics
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

    def evaluate(self, models_dir: str) -> dict:
        results = []
        for file_name in os.listdir(models_dir):
            if ".npy" not in file_name:
                if 'fasttext' in file_name:
                    model = FastText.load(os.path.join(models_dir, file_name))
                else:
                    model = Word2Vec.load(os.path.join(models_dir, file_name))

                positions = []
                marks = []

                for analogy in self.analogies():
                    try:
                        similars = model.wv.most_similar(negative=[analogy[0]], positive=[analogy[1], analogy[2]])
                    except KeyError:
                        positions.append(-1)
                        marks.append(0)
                    else:
                        similar = next(((index, tuple) for (index, tuple) in enumerate(similars) if tuple[0] == analogy[3]), None)
                        if similar is None:
                            positions.append(-1)
                            marks.append(0)
                        else:
                            positions.append(similar[0])
                            marks.append(similar[1][1])

                results.append(
                    {
                        "model": file_name,
                        "window": model.window,
                        "vector_size": model.vector_size,
                        "positions": positions,
                        "marks": marks,
                        "accuracy": statistics.mean(marks)
                    }
                )

        return results
