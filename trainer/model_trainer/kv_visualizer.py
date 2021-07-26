import os


if __name__ == '__main__':

    import sys
    from gensim.models import Word2Vec, FastText
    
    
    if len(sys.argv) == 3:

        # Load the model
        if sys.argv[2] == 0:
            model = Word2Vec.load(sys.argv[1])
        else:
            model = FastText.load(sys.argv[1])
        
        keyedvectors = model.wv

        modelpath, modelname = os.path.split(sys.argv[1])

        
        # Vector file, `\t` seperated the vectors and `\n` seperate the words
        """
        0.1\t0.2\t0.5\t0.9
        0.2\t0.1\t5.0\t0.2
        0.4\t0.1\t7.0\t0.8
        """
        out_v = open(os.path.join(modelpath, modelname + '_vecs.tsv'), 'w', encoding='utf-8')


        # Meta data file, `\n` seperated word
        """
        token1
        token2
        token3
        """
        out_m = open(os.path.join(modelpath, modelname + '_meta.tsv'), 'w', encoding='utf-8')


        # Write meta file and vector file
        for index in range(len(keyedvectors.index_to_key)):
            word = keyedvectors.index_to_key[index]
            vec = keyedvectors.vectors[index]
            out_m.write(word + "\n")
            out_v.write('\t'.join([str(x) for x in vec]) + "\n")
        
        out_v.close()
        out_m.close()

        # Then we can visuale using the `http://projector.tensorflow.org/` to visualize those two files.
        # 1. Open the Embedding Projector.
        # 2. Click on "Load data".
        # 3. Upload the two files we created above: vecs.tsv and meta.tsv.