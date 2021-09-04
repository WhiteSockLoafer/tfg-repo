from gensim.models import Word2Vec
from lib import AnalogiesDatasetReader


model = Word2Vec.load('trainer/model_trainer/out/models/word2vec_14.model')
dataset = AnalogiesDatasetReader('trainer/analogies/dataset')

for i, analogy in enumerate(dataset.analogies()):
    try:
        similars = model.wv.most_similar(negative=[analogy[0]], positive=[
                                         analogy[1], analogy[2]], topn=8)
    except KeyError as e:
        print('El token "' + e.args[0] + '" no esta presente en el vocabulario')
    else:
        print('"' + analogy[0] + '" es a "' + analogy[1] + '" lo que "' + analogy[2] + '" es a ...')
        print(similars)
        print('Respuesta correcta "' + analogy[3] + '"\n')
