from gensim.models import Word2Vec


model = Word2Vec.load('trainer/model_trainer/out/models/word2vec_8.model')

print(model.wv.most_similar(negative=['magistrado'], positive=['tribunal', 'juez'], topn=8))