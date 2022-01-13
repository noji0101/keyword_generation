import numpy as np

def read_synset(synset_filepath):
    with open(synset_filepath) as f:
        sysnet_text = f.read().splitlines()
    sysnet_text = [i.split(' ') for i in sysnet_text]
    sysnet_text = sysnet_text[1:]
    synset_dict = {}
    for line in sysnet_text:
        synset_dict[line[0]] = np.array([np.float64(i) for i in line[1:]])
    return synset_dict

def read_lexemes_dict_and_list(lexemes_filepath):
    with open(lexemes_filepath) as f:
        lexemes_text = f.read().splitlines()
    lexemes_text = [i.split(' ') for i in lexemes_text][1:]
    lexemes_dict = {}
    lexemes_list = []
    for line in lexemes_text:
        lexemes_dict[line[0]] = np.array([np.float64(i) for i in line[1:]])
        lexemes_list.append([line[0], np.array([np.float64(i) for i in line[1:]])])
    return lexemes_dict, lexemes_list

def read_mapping(mapping_filepath):
    with open(mapping_filepath) as f:
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