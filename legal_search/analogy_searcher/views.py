from django.shortcuts import render
from django.template import loader
from gensim.models import Word2Vec

model = Word2Vec.load('/home/jrc/Universidad/2020-2021/2_TFG/tfg-repo/legal_search/analogy_searcher/w2v_model/word2vec_8.model')

def index(request):
    return render(request, 'analogy_searcher/index.html')

def predict(request):
    tuples = model.wv.most_similar(negative=[request.POST['n1']], positive=[request.POST['p1'], request.POST['p2']])
    result_list = [t[0] for t in tuples]
    return render(request, 'analogy_searcher/index.html', 
    context= {
        "result_list": result_list
    })
