import math
import random
import pickle
import gensim

topword = 20 # ?
word2vec_filepath = 'data/GoogleNews-vectors-negative300.bin'
word2vec_model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_filepath, binary=True)
def generate_similar_space(space_name, main_list, renkan):

    for i in range(1):# ????
        wordlist = []
        # ランダムに選択する
        n_random = math.floor(random.uniform(0, len(main_list)))
        n_random = 0  # ここを消せばランダムなる

        入力単語集合 = [main_list[n_random]]
        
        # 最も類似度が高い単語を抽出
        kyouki = word2vec_model.most_similar(positive=入力単語集合, topn=topword)

        # 記録リストの調整
        for result in kyouki:
            wordlist.append(result[0])  # 結果からワードだけを取り出している，値だけでも可能
        print(space_name + '空間内での共起') # space_nameは価値、意味、状態、属性のどれか
        print(main_list[n_random])
        print(wordlist, end='')


        # topword:一度に提示する共起単語の数
        for j in range(topword):
            # 重複チェック
            if not wordlist[j] in value_list and \
            not wordlist[j] in mean_list and \
            not wordlist[j] in state_list and \
            not wordlist[j] in attr_list:
                # if not wordlist[j] in usedv and not wordlist[j] in usedm and not wordlist[j] in useds and not wordlist[j] in useda:
                main_list.append(wordlist[j])  # 今まで共起した単語と重複しないj+1番めの順位の共起語を持ってくる
                renkan.append([main_list[n_random], wordlist[j]])
                break

    print('採用された単語：' + wordlist[j]) # ??
    print(renkan)

# 与えられた属性要素，状態要素から新たな状態要素を発想 seni=遷移
def generate_different_space(x, beforelist, afterlist, renkan):

    r_random = math.floor(random.uniform(0, len(renkan)))
    bn_random = math.floor(random.uniform(1, len(beforelist)))

    # renkan[r_random][0] #価値1
    # 選択した連関と選ばれた単語が等しい場合だめなので、異なるまでランダムを回す
    if x == '属性から状態' or x == '状態から意味' or x == '意味から価値':  # 要するに下から上の場合
        while renkan[r_random][1] == beforelist[bn_random]:  
            r_random = math.floor(random.uniform(0, len(renkan)))
            bn_random = math.floor(random.uniform(1, len(beforelist)))
    else:  # 要するに上から下の場合
        while renkan[r_random][0] == beforelist[bn_random]:
            r_random = math.floor(random.uniform(0, len(renkan)))
            bn_random = math.floor(random.uniform(1, len(beforelist)))

    # 既存1-既存2+発生源1=新要素
    r_random = 0  # ここを消せばランダムな連関が選択される 0にすると自分で入力した要素の連関

    if x == '属性から状態' or x == '状態から意味' or x == '意味から価値':  # 要するに下から上の場合
        words_positive = [renkan[r_random][0], beforelist[bn_random]]
        word_negetive = [renkan[r_random][1]]

        kyouki = word2vec_model.most_similar(positive=words_positive, negative=word_negetive, topn=topword)

    else:  # 要するに上から下の場合
        words_positive = [renkan[r_random][1], beforelist[bn_random]]
        word_negetive = [renkan[r_random][0]]

        kyouki = word2vec_model.most_similar(positive=words_positive, negative=word_negetive, topn=topword)

    # 共起を表示する
    wordlist = []
    for result in kyouki:
        wordlist.append(result[0])
    print(x + 'を発想')
    if x == '属性から状態' or x == '状態から意味' or x == '意味から価値':  # 要するに下から上の場合
        print(renkan[r_random][1] + ' - ' + renkan[r_random][0] + ' + ' + beforelist[bn_random])
    else:
        print(renkan[r_random][1] + ' - ' + renkan[r_random][0] + ' + ' + beforelist[bn_random])
    print(wordlist, end='')

    # リストの調整
    # afuse.append(afterlist[0])
    # afterlist.remove(afterlist[0])
    for j in range(topword):
        # 重複チェック
        if not wordlist[j] in value_list \
        and not wordlist[j] in mean_list \
        and not wordlist[j] in state_list \
        and not wordlist[j] in attr_list:
            # if not wordlist[j] in usedv and not wordlist[j] in usedm and not wordlist[j] in useds and not wordlist[j] in useda:
            afterlist.append(wordlist[j])  # 重複した場合j番めの順位の共起語を持ってくる
            break
    print('採用された単語：' + wordlist[j])
    # 連関の記録
    if x == '属性から状態' or x == '状態から意味' or x == '意味から価値':
        renkan.append([wordlist[j], beforelist[bn_random]])
    else:
        renkan.append([beforelist[bn_random], wordlist[j]])


renkan = []
value_list = ['safety']
mean_list = ['toughness']
state_list = ['velocity']
attr_list = ['tire']
generate_similar_space('value', value_list, renkan)
generate_similar_space('meaning', mean_list, renkan)
generate_similar_space('state', state_list, renkan)
generate_similar_space('attribute', attr_list, renkan)

generate_different_space('意味から価値', mean_list, value_list, renkan)
