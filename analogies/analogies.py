from gensim.models import Word2Vec


model = Word2Vec.load('models/word2vec_1.model')

print('hombre es a hombres lo que mujer es a ...')
print(model.wv.most_similar(negative=['hombre'], positive=['hombres', 'mujer'])) # MUJERES - PRURALIDAD
print('\n')

print('padre es a madre lo que hijo es a ...')
print(model.wv.most_similar(negative=['padre'], positive=['madre', 'hijo'])) # HIJA - GENEROS
print('\n')

print('mancomunado es a solidario lo que dolo es a ...')
print(model.wv.most_similar(negative=['mancomunado'], positive=['solidario', 'dolo'])) # CULPA - CONTRARIOS
print('\n')

print('negligencia es a diligencia lo que directos es a ...')
print(model.wv.most_similar(negative=['negligencia'], positive=['diligencia', 'directos'])) # INDIRECTOS - CONTRARIOS
print('\n')

print('agravar es a atenuar lo que favorable es a ...')
print(model.wv.most_similar(negative=['agravar'], positive=['atenuar', 'favorable'])) # DESFAVORABLE - CONTRARIOS
print('\n')

print('favorable es a desfavorable lo que atenuar es a ...')
print(model.wv.most_similar(negative=['favorable'], positive=['desfavorable', 'atenuar'])) # AGRAVAR - CONTRARIOS
print('\n')

print('corts es a cortes lo que consell es a ...')
print(model.wv.most_similar(negative=['corts'], positive=['cortes', 'consell'])) # CONSEJO - TRADUCCIÓN CATALÁN
print('\n')

print('agresión es a abuso lo que robo es a ...')
print(model.wv.most_similar(negative=['agresión'], positive=['abuso', 'robo'])) # HURTO - MAYOR MENOR GRADO
print('\n')

print('congreso es a diputados lo que senado es a ...')
print(model.wv.most_similar(negative=['congreso'], positive=['diputados', 'senado'])) # SENADORES - RELACIÓN DE PERTENENCIA
print('\n')

print('acción es a omisión lo que activo es a ...')
print(model.wv.most_similar(negative=['acción'], positive=['omisión', 'activo'])) # PASIVO - CONTRARIOS
print('\n')