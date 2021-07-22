from gensim.models import Word2Vec


model = Word2Vec.load('models/fasttext_1.model')

print('hombre es a hombres lo que mujer es a ...')
print(model.wv.most_similar(negative=['hombre'], positive=['hombres', 'mujer'])) # MUJERES - PRURALIDAD
print('\n')