"""
@author: BrikerMan
@contact: eliyar917@gmail.com
@blog: https://eliyar.biz
@version: 1.0
@license: Apache Licence
@file: w2v_visualizer.py
@time: 2017/7/30 上午9:37
"""

from gensim.models import KeyedVectors

# Load gensim word2vec
w2v_path = 'modelo/boe.wordvectors'
w2v = KeyedVectors.load(w2v_path)

import io

# Vector file, `\t` seperated the vectors and `\n` seperate the words
"""
0.1\t0.2\t0.5\t0.9
0.2\t0.1\t5.0\t0.2
0.4\t0.1\t7.0\t0.8
"""
out_v = io.open('modelo/vecs.tsv', 'w', encoding='utf-8')

# Meta data file, `\n` seperated word
"""
token1
token2
token3
"""
out_m = io.open('modelo/meta.tsv', 'w', encoding='utf-8')

# Write meta file and vector file
for index in range(len(w2v.index_to_key)):
    word = w2v.index_to_key[index]
    vec = w2v.vectors[index]
    out_m.write(word + "\n")
    out_v.write('\t'.join([str(x) for x in vec]) + "\n")
out_v.close()
out_m.close()

# Then we can visuale using the `http://projector.tensorflow.org/` to visualize those two files.

# 1. Open the Embedding Projector.
# 2. Click on "Load data".
# 3. Upload the two files we created above: vecs.tsv and meta.tsv.