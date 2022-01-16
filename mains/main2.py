import itertools
import numpy as np
import random

from word_extractor.lexemes_vector import get_most_similar_lexemes, get_verctor_from_word, get_verctor_from_sense_key, get_word_from_vector, get_analogy
from word_extractor.wordnet import get_hypernum, get_hyponym, get_not_similar_hyponym
from word_extractor.word2vec_extractor import analogy_by_word2vec


def extract_words_2(input_words, word2vec):
    """
    word2vec(比較用)
    """

    extracted_words = []
    links = []
    word_histries = []
    word_histries_2 = []

    # 機能1〜4
    for input_word in input_words:
        num_words = len(extracted_words)
        extracted_words.append({'id':num_words, 'label':input_word, 'function':0})
        word_histries.append(input_word)
        
        # 抽出
        try:
            indices  = rand_ints_nodup(0, 9, 4)
            word2vec_words = word2vec.most_similar([input_word])
            word1, word2, word3, word4 = [word2vec_words[idx][0] for idx in indices]
            print(word1, word2, word3, word4)
            for word in [word1, word2, word3, word4]:
                word_histries.append(word)
            word_histries_2.append([input_word, word1, word2, word3, word4])

            # エッジを定義
            count = 0
            for i, output_word in enumerate([word1, word2, word3, word4]):
                if output_word is None:
                    # print('Got None')
                    pass
                else:
                    count += 1
                    input_id = num_words
                    output_id = input_id + count
                    extracted_words.append({'id':output_id, 'label':output_word, 'function':10})
                    links.append({'source':input_id, 'target':output_id})
        except KeyError:
            pass

    # 機能5(1つの入力単語から)
    print('機能５-１')
    for idx in range(int(len(word_histries) / 5)):
        id_input = check_id(idx*5, word_histries)
        input_word, word1, word2, word3, word4 = word_histries[5*idx:5*idx+5]
        for i, word in enumerate([word1, word4]):
            # 類推の計算
            output_word = analogy_by_word2vec(input_word, word3, word, word2vec)
            wordlist = [word_dic.get('label') for word_dic in extracted_words]
            if (not output_word in wordlist) and (output_word is not None):
                id_output = len(extracted_words)
                extracted_words.append({'id':id_output, 'label':output_word, 'function':11})
                links.append({'source':id_input, 'target':id_output})

    # 機能5(2つの入力単語の組み合わせ)
    # 組み合わせをランダム6こ選ぶ
    num_input_words = len(input_words)
    combi_all = list(itertools.combinations(range(num_input_words), 2))
    idx_conbi = rand_ints_nodup(0, len(combi_all)-1, 6)
    combi_list = [combi_all[idx] for idx in idx_conbi]

    print('機能５-２')
    for idx1, idx2 in combi_list:
        id_input_1 = check_id(idx1*5, word_histries)
        id_input_2 = check_id(idx2*5, word_histries)

        input_word_idx1, word1_idx1, word2_idx1, word3_idx1, word4_idx1 = word_histries_2[idx1]
        input_word_idx2, word1_idx2, word2_idx2, word3_idx2, word4_idx2 = word_histries_2[idx2]
        
        for word in [input_word_idx2, word1_idx2, word2_idx2, word3_idx2, word4_idx2]:
            
            output_word = analogy_by_word2vec(input_word_idx1, word2_idx1, word, word2vec)
            wordlist = [word_dic.get('label') for word_dic in extracted_words]
            if (not output_word in wordlist) and (output_word is not None):
                id_output = len(extracted_words)
                extracted_words.append({'id':id_output, 'label':output_word, 'function':11})
                links.append({'source':id_input_1, 'target':id_output})
                links.append({'source':id_input_2, 'target':id_output})

    return extracted_words, links

def check_id(idx, word_histries):
    num_none = word_histries[:idx].count(None)
    id = idx - num_none
    return id

def rand_ints_nodup(a, b, k):
    ns = []
    while len(ns) < k:
        n = random.randint(a, b)
        if not n in ns:
            ns.append(n)
    return ns