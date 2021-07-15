import os
from django.shortcuts import render
from django.conf import settings
from gensim.models import Word2Vec

model = Word2Vec.load(os.path.join(settings.BASE_DIR, 'analogy_searcher/w2v_model/word2vec_8.model'))

def index(request):
    return render(request, 'predict.html')

def predict(request):
    tuples = model.wv.most_similar(negative=[request.POST['n1']], positive=[request.POST['p1'], request.POST['p2']])
    result_list = [t[0] for t in tuples]
    return render(request, 'predict.html', 
    context= {
        "result_list": result_list
    })
