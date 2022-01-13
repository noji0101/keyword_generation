import itertools
import numpy as np
import random

from word_extractor.lexemes_vector import get_most_similar_lexemes, get_verctor_from_word, get_verctor_from_sense_key, get_word_from_vector, get_analogy
from word_extractor.wordnet import get_hypernum, get_hyponym, get_not_similar_hyponym


def extract_words_3(input_words, lexemes_dict, lexemes_list, mapping_dict):
    """
    類似度のみ
    """

    extracted_words = []
    links = []
    word_histries = []

    # 機能1〜4
    for input_word in input_words:
        num_words = len(extracted_words)
        extracted_words.append({'id':num_words, 'label':input_word, 'function':0})
        word_histries.append(input_word)

        # 抽出
        word4, _ = get_most_similar_lexemes(input_word, lexemes_dict, lexemes_list, mapping_dict)
        print(word4)
        for word in [word4]:
            word_histries.append(word)

        # エッジを定義
        count = 0
        for i, output_word in enumerate([word4]):
            if output_word is None:
                # print('Got None')
                pass
            else:
                count += 1
                input_id = num_words
                output_id = input_id + count
                extracted_words.append({'id':output_id, 'label':output_word, 'function':i+1})
                links.append({'source':input_id, 'target':output_id})

    return extracted_words, links