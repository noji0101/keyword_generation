import random

import numpy as np
from scipy.spatial import distance
import nltk
from nltk.corpus import wordnet 
nltk.download("wordnet")


class AutoextendExtractor():

    def __init__(self, lexemes_filepath, mapping_filepath):
        self.lexemes_filepath = lexemes_filepath
        self.mapping_filepath = mapping_filepath

        self.lexemes_dict, self.lexemes_list = self.read_lexemes_dict_and_list()
        self.mapping_dict = self.read_mapping()


    def get_most_similar_lexemes(self, word, rank_range=10, num_word=1, synset_idx=0):
        vector = self.get_verctor_from_word(word, synset_idx)
        if vector is not None:
            all_vectors = [lexeme[1] for lexeme in self.lexemes_list]
            cos_similarities = 1 - distance.cdist([vector], all_vectors, metric='cosine')[0]
            sorted_indices = np.argsort(cos_similarities)[::-1]
            most_similar_lexemes = []
            for i in range(rank_range):
                idx = sorted_indices[i+1] 
                most_similar_lexeme = self.lexemes_list[idx][0]
                cos_similarity = cos_similarities[idx]
                most_similar_lexemes.append([most_similar_lexeme, cos_similarity])

            output_lexemes = []
            indices = self.rand_ints_nodup(0, rank_range-1, num_word)
            for idx in indices:
                output_lexeme = most_similar_lexemes[idx][0][:-18]
                output_synset_name = most_similar_lexemes[idx][0][-17:]
                output_sense_keys = self.mapping_dict[output_synset_name]
                output_sense_key = None
                for sense_key_temp in output_sense_keys:
                    if output_lexeme in sense_key_temp.lower():
                        output_sense_key = sense_key_temp
                output_lexemes.append([output_lexeme, output_sense_key])
            return output_lexemes
        else:
            output = [[None, None] for _ in range(num_word)]
            return output

    def get_verctor_from_word(self, word, synset_idx=0):
        try:
            sense_key = wordnet.synsets(word)[synset_idx].lemmas()[0].key()
            vector_key = self.get_key_from_value(self.mapping_dict, sense_key)
        
            lexemes_vector = self.lexemes_dict[f'{word}-{vector_key}']
            return lexemes_vector
        except (KeyError, IndexError, AttributeError):
            return None

    def get_verctor_from_sense_key(self, sense_key):
        try:
            word = sense_key[:-10]
            vector_key = self.get_key_from_value(self.mapping_dict, sense_key)
            lexemes_vector = self.lexemes_dict[f'{word}-{vector_key}']
            return lexemes_vector
        except (KeyError, IndexError, TypeError):
            return None
        
    def get_key_from_value(self, dic, val):
        for key, sense_keys in dic.items():
            for sense_key in sense_keys:
                if sense_key == val:
                    return key
        return None
    
    def get_senseky_from_word(self, word, synset_idx=0):
        try:
            sense_key = wordnet.synsets(word)[synset_idx].lemmas()[0].key()
            return sense_key
        except (KeyError, IndexError, AttributeError):
            return None

    def get_word_from_vector(self, vector):
        all_vectors = [lexeme[1] for lexeme in self.lexemes_list]
        cos_similarities = 1 - distance.cdist([vector], all_vectors, metric='cosine')[0]
        
        sorted_indices = np.argsort(cos_similarities)[::-1]
        indices = sorted_indices[:10] 
        most_similar_lexemes = []
        for idx in indices:
            most_similar_lexemes.append(self.lexemes_list[idx][0][:-18])
        
        return most_similar_lexemes

    def get_analogy(self, word1, word2, word3):
        word1_vec = self.get_verctor_from_word(word1)
        word2_vec = self.get_verctor_from_word(word2)
        word3_vec = self.get_verctor_from_word(word3)

        if (word1_vec is not None) and (word2_vec is not None) and (word3_vec is not None):
            words = self.get_word_from_vector(word1_vec - word2_vec + word3_vec)
            output_word = None
            for word in words:
                if (word != word1) and (word != word2) and (word != word3):
                    output_word = word
                    break
            print(f'{word1} - {word2} + {word3} = {output_word}')
            return output_word
        else:
            print('None')
            return None

    def get_analogy_by_sensekey(self, word1_sensekey, word2_sensekey, word3_sensekey):
        word1, word2, word3 = [word1_sensekey[:-10], word2_sensekey[:-10], word3_sensekey[:-10]]

        word1_vec = self.get_verctor_from_sense_key(word1_sensekey)
        word2_vec = self.get_verctor_from_sense_key(word2_sensekey)
        word3_vec = self.get_verctor_from_sense_key(word3_sensekey)

        output_word = None
        if (word1_vec is not None) and (word2_vec is not None) and (word3_vec is not None):
            words = self.get_word_from_vector(word1_vec - word2_vec + word3_vec)
            for word in words:
                if (word != word1) and (word != word2) and (word != word3):
                    output_word = word
                    break
            print(f'{word1} - {word2} + {word3} = {output_word}')
            return output_word
        else:
            print('None')
            return None

    def read_lexemes_dict_and_list(self):
        with open(self.lexemes_filepath) as f:
            lexemes_text = f.read().splitlines()
        lexemes_text = [i.split(' ') for i in lexemes_text][1:]
        lexemes_dict = {}
        lexemes_list = []
        for line in lexemes_text:
            lexemes_dict[line[0]] = np.array([np.float64(i) for i in line[1:]])
            lexemes_list.append([line[0], np.array([np.float64(i) for i in line[1:]])])
        return lexemes_dict, lexemes_list

    def read_mapping(self):
        with open(self.mapping_filepath) as f:
            mapping_text = f.read().splitlines()
        mapping_dict = {}
        for line in mapping_text:
            if len(line) == 18:
                synset_name = line[:-1]
                mapping_dict[synset_name] = ['']
            else:
                synset_name = line.split(' ')[0]
                sense_key = [lexeme for lexeme in (line.split(' ')[1]).split(',')][:-1]
                mapping_dict[synset_name] = sense_key
        return mapping_dict

    def rand_ints_nodup(self, a, b, k):
        ns = []
        while len(ns) < k:
            n = random.randint(a, b)
            if not n in ns:
                ns.append(n)
        return ns






def get_most_similar_lexemes(word, lexemes_dict, lexemes_list, mapping_dict, rank_range=10, num=1, synset_idx=0):
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
