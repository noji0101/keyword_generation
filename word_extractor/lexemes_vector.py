import random

import numpy as np
from scipy.spatial import distance
import nltk
from nltk.corpus import wordnet 
nltk.download("wordnet")


def get_most_similar_lexemes(word, lexemes_dict, lexemes_list, mapping_dict, rank_range=10, is_single=True, synset_idx=0):
    vector = get_verctor_from_word(word, lexemes_dict, mapping_dict, synset_idx)
    if vector is not None:
        all_vectors = [lexeme[1] for lexeme in lexemes_list]
        cos_similarities = 1 - distance.cdist([vector], all_vectors, metric='cosine')[0]
        sorted_indices = np.argsort(cos_similarities)[::-1]
        most_similar_lexemes = []
        for i in range(rank_range):
            idx = sorted_indices[i+1] 
            most_similar_lexeme = lexemes_list[idx][0]
            cos_similarity = cos_similarities[idx]
            most_similar_lexemes.append([most_similar_lexeme, cos_similarity])
        if is_single:
            n_random = random.randint(0, len(most_similar_lexemes)-1)
            most_similar_lexeme = most_similar_lexemes[n_random][0][:-18]
            synset_name = most_similar_lexemes[n_random][0][-17:]
            sense_keys = mapping_dict[synset_name]
            sense_key = None
            for sense_key_temp in sense_keys:
                if most_similar_lexeme in sense_key_temp.lower():
                    sense_key = sense_key_temp
            
            return most_similar_lexeme, sense_key
        else:
            return most_similar_lexemes, None
    else:
        return None, None

def get_verctor_from_word(word, lexemes_dict, mapping_dict, synset_idx=0):
    try:
        sense_key = wordnet.synsets(word)[synset_idx].lemmas()[0].key()
        vector_key = get_key_from_value(mapping_dict, sense_key)
    
        lexemes_vector = lexemes_dict[f'{word}-{vector_key}']
        return lexemes_vector
    except (KeyError, IndexError, AttributeError):
        return None

def get_verctor_from_sense_key(sense_key, lexemes_dict, mapping_dict):
    try:
        word = sense_key[:-10]
        vector_key = get_key_from_value(mapping_dict, sense_key)
    
        lexemes_vector = lexemes_dict[f'{word}-{vector_key}']
        return lexemes_vector
    except (KeyError, IndexError, TypeError):
        return None
    
def get_key_from_value(dic, val):
    for key, sense_keys in dic.items():
        for sense_key in sense_keys:
            if sense_key == val:
                return key
    return None

def get_word_from_vector(vector, lexemes_list):
    all_vectors = [lexeme[1] for lexeme in lexemes_list]
    cos_similarities = 1 - distance.cdist([vector], all_vectors, metric='cosine')[0]
    
    sorted_indices = np.argsort(cos_similarities)[::-1]
    indices = sorted_indices[:10] 
    most_similar_lexemes = []
    for idx in indices:
        most_similar_lexemes.append(lexemes_list[idx][0][:-18])
    
    return most_similar_lexemes

def get_analogy(word1, word2, word3, lexemes_dict, lexemes_list, mapping_dict):
    word1_vec = get_verctor_from_word(word1, lexemes_dict, mapping_dict)
    word2_vec = get_verctor_from_word(word2, lexemes_dict, mapping_dict)
    word3_vec = get_verctor_from_word(word3, lexemes_dict, mapping_dict)

    if (word1_vec is not None) and (word2_vec is not None) and (word3_vec is not None):
        words = get_word_from_vector(word1_vec - word2_vec + word3_vec, lexemes_list)
        for word in words:
            if (word != word1) and (word != word2) and (word != word3):
                output_word = word
                break
        print(f'{word1} - {word2} + {word3} = {output_word}')
        return output_word
    else:
        print('None')
        return None