from gensim.models.word2vec import Word2Vec


model = Word2Vec.load('modelo/boe.model')

print(model.wv.most_similar(negative=['hombre'], positive=['hombres', 'mujer'])) # MUJERES - PRURALIDAD
print('\n')
print(model.wv.most_similar(negative=['padre'], positive=['madre', 'hijo'])) # HIJA - GENEROS
print('\n')
print(model.wv.most_similar(negative=['mancomunado'], positive=['solidario', 'dolo'])) # CULPA - CONTRARIOS
print('\n')
print(model.wv.most_similar(negative=['negligencia'], positive=['diligencia', 'directos'])) # INDIRECTOS - CONTRARIOS
print('\n')
print(model.wv.most_similar(negative=['agravar'], positive=['atenuar', 'favorable'])) # DESFAVORABLE - CONTRARIOS
print('\n')
print(model.wv.most_similar(negative=['favorable'], positive=['desfavorable', 'atenuar'])) # AGRAVAR - CONTRARIOS
print('\n')
print(model.wv.most_similar(negative=['corts'], positive=['cortes', 'consell'])) # CONSEJO - TRADUCCIÓN CATALÁN
print('\n')
print(model.wv.most_similar(negative=['agresión'], positive=['abuso', 'robo'])) # HURTO - MAYOR MENOR GRADO
print('\n')
print(model.wv.most_similar(negative=['congreso'], positive=['diputados', 'senado'])) # SENADORES - RELACIÓN DE PERTENENCIA
print('\n')
print(model.wv.most_similar(negative=['acción'], positive=['omisión', 'activo'])) # PASIVO - CONTRARIOS
print('\n')