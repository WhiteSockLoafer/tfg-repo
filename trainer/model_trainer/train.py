import os
import sys
import json
from lib import DirectoryCorpusReader, AnalogiesDatasetReader, makeplots
import time
from gensim.models import Word2Vec, FastText


if __name__ == '__main__':

    if len(sys.argv) == 3 and not os.path.exists('./out'):

        corpus = DirectoryCorpusReader(dir_path=sys.argv[1])
        dataset = AnalogiesDatasetReader(dataset_path=sys.argv[2])
        models_dir = './out/models'
        os.makedirs('./out')
        os.makedirs(models_dir)

        vector_sizes = [200, 500]
        windows = [1, 4]

        init_time = time.time()

        i = 0

        for vector_size in vector_sizes:
            for window in windows:

                print('Preparing models with:')
                print('\tVECTOR SIZE -> ' + str(vector_size))
                print('\tWINDOW -> ' + str(window) + '\n')

                i += 1
                print('Training model ' + str(i) + '/' + str(len(vector_sizes) * len(windows) * 2) + '...')
                partial_time = time.time()
                model = FastText(sentences=corpus, vector_size=vector_size, window=window, min_count=10, workers=8)
                print(f'Time taken : {(time.time() - partial_time) / 60:.2f} mins')
                model.save(models_dir + '/fasttext_' + str(i) + '.model')
                print('Model fasttext_' + str(i) + ' saved\n')

                i += 1
                print('Training model ' + str(i) + '/' + str(len(vector_sizes) * len(windows) * 2) + '...')
                partial_time = time.time()
                model = Word2Vec(sentences=corpus, vector_size=vector_size, window=window, min_count=10, workers=8)
                print(f'Time taken : {(time.time() - partial_time) / 60:.2f} mins')
                model.save(models_dir + '/word2vec_' + str(i) + '.model')
                print('Model word2vec_' + str(i) + ' saved\n')

        print('Evaluating the models...')
        partial_time = time.time()
        results = dataset.evaluate(models_dir=models_dir, topn=8)
        plot = makeplots(results)
        plot.savefig("out/figure.png")
        with open('out/results.json', 'w') as f:
            json.dump(results, f)
        print(f'Time taken : {(time.time() - partial_time) / 60:.2f} mins')
        print('Results report saved in ./out\n')

        print(f'Total time taken : {(time.time() - init_time) / 60:.2f} mins\n')
