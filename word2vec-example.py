#!/bin/python3
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format("entity_vector/entity_vector.model.bin", binary=True)
print(model.most_similar("寿司"))
