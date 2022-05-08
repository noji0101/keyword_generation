import random

import numpy as np
import nltk
from nltk.corpus import wordnet
nltk.download("wordnet")
from scipy.spatial import distance

from word_extractor.lexemes_vector import AutoextendExtractor


def get_hypernum(word, idx=0, distance=1):
    synsets = wordnet.synsets(word)
    try:
        synset = synsets[idx]
    except IndexError:
        return None, None
    if (synset.name().split('.')[1] == 'a') or (synset.name().split('.')[1] == 'v'):
        synset = to_noun(synset)
    try:
        hypernum = synset.hypernym_paths()[0][-(distance+1)]
    except IndexError:
        
        return None, None
    sense_key = hypernum.lemmas()[0].key()
    hypernum_lexemes = hypernum.lemmas()[0].key()[:-10]
    return hypernum_lexemes, sense_key

def get_hyponym(word, idx=0):
    synsets = wordnet.synsets(word)
    try:
        synset = synsets[idx]
    except IndexError:
        # print("No such word")
        return None, None
    if (synset.name().split('.')[1] == 'a') or (synset.name().split('.')[1] == 'v'):
        synset = to_noun(synset)

    hyponyms = synset.hyponyms()
    if not hyponyms:
        # print("No hyponyms")
        return None, None
    else:
        n_random = random.randint(0, len(hyponyms)-1)
        hyponym = hyponyms[n_random]
        sense_key = hyponym.lemmas()[0].key()
        hyponym_lexemes = hyponym.lemmas()[0].key()[:-10]
        return hyponym_lexemes, sense_key

def get_not_similar_hyponym(input_word, autoextend: AutoextendExtractor, idx=0):
    '''
    下位の中で，語義ベクトルの類似度が低い単語の抽出
    '''
    input_word_vector = autoextend.get_verctor_from_word(input_word)
    if input_word_vector is not None:
        synsets = wordnet.synsets(input_word)
        try:
            synset = synsets[idx]
        except IndexError:
            # print("No such word")
            return None, None 
        if (synset.name().split('.')[1] == 'a') or (synset.name().split('.')[1] == 'v'):
            print(synset.name().split('.')[1])
            synset = to_noun(synset)

        hyponyms = synset.hyponyms()
        if not hyponyms:
            # print("No hyponyms")
            return None, None
        else:
            sense_keys = [hyponym.lemmas()[0].key() for hyponym in hyponyms]
            vectors_keys = [autoextend.get_key_from_value(autoextend.mapping_dict, sense_key) for sense_key in sense_keys]
            words = [sense_key[:-10] for sense_key in sense_keys]
            lexemes_vectors = []
            words_not_none = []
            for vector_key, word in zip(vectors_keys, words):
                try:
                    lexemes_vectors.append(autoextend.lexemes_dict[f'{word}-{vector_key}'])
                    words_not_none.append(word)
                except (KeyError, ValueError):
                    # print('skipped')
                    pass
            try:
                cos_similarities = 1 - distance.cdist([input_word_vector], lexemes_vectors, metric='cosine')[0]
                most_similar_idx = np.argmin(cos_similarities)
                sense_key = sense_keys[most_similar_idx]
                hyponym_lexemes = words_not_none[most_similar_idx]
            except ValueError:
                return None, None

            return hyponym_lexemes, sense_key
    else:
        return None, None

def to_noun(synset):
    try:
        synset = synset.lemmas()[0].derivationally_related_forms()[0].synset()
    except IndexError:
        pass
    return  synset