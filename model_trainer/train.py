import sys
from lib import DirectoryCorpusReader, AnalogiesDatasetReader
import time
from gensim.models import Word2Vec, FastText


if __name__ == '__main__':

    if len(sys.argv) == 4:

        corpus = DirectoryCorpusReader(dir_path=sys.argv[1])
        dataset = AnalogiesDatasetReader(dataset_path=sys.argv[2])
        models_dir = sys.argv[3]

        vector_sizes = [300]
        windows = [5]

        init_time = time.time()

        for i, vector_size in enumerate(vector_sizes):
            for j, window in enumerate(windows):

                print('Preparing models with:')
                print('\tVECTOR SIZE -> ' + str(vector_size))
                print('\tWINDOW -> ' + str(window) + '\n')

                print('Training FastText model ' + str((i+j)*2+1) + '/' + str(len(vector_sizes) * len(windows) * 2) + '...')
                partial_time = time.time()
                model = FastText(sentences=corpus, vector_size=vector_size, window=window, min_count=10, workers=8)
                print(f'Time taken : {(time.time() - partial_time) / 60:.2f} mins')
                model.save(models_dir + '/fasttext_' + str((i+j)*2+1) + '.model')
                print('Model fasttext_' + str((i+j)*2+1) + ' saved\n')

                print('Training Word2Vec model ' + str((i+j)*2+2) + '/' + str(len(vector_sizes) * len(windows) * 2) + '...')
                partial_time = time.time()
                model = Word2Vec(sentences=corpus, vector_size=vector_size, window=window, min_count=10, workers=8)
                print(f'Time taken : {(time.time() - partial_time) / 60:.2f} mins')
                model.save(models_dir + '/word2vec_' + str((i+j)*2+1) + '.model')
                print('Model word2vec_' + str((i+j)*2+1) + ' saved\n')

        print(f'Total time taken : {(time.time() - init_time) / 60:.2f} mins\n')