import os
from django.shortcuts import render
from django.conf import settings
from gensim.models import Word2Vec

model = Word2Vec.load(os.path.join(
    settings.BASE_DIR, 'analogy_searcher/w2v_model/word2vec_14.model'
))


def predict(request):
    if request.method == 'POST':
        tuples = model.wv.most_similar(negative=[request.POST['n1']], positive=[
                                       request.POST['p1'], request.POST['p2']], topn=8)
        final_list = []
        for t in tuples:
            final_list.append((t[0], int(t[1] * 100)))

        return render(request, 'post_predict.html', context={
            "result_list": final_list,
            "n1": request.POST['n1'],
            "p1": request.POST['p1'],
            "p2": request.POST['p2']

        })
    else:
        return render(request, 'get_predict.html')
