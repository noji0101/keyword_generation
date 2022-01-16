def analogy_by_word2vec(word1, word2, word3, word2vec):
    results = word2vec.most_similar(positive=[word1, word3],negative=[word2])
    output_word = None
    for result_word in results:
        print(result_word)
        result_word = result_word[0]
        print(result_word)
        if (result_word != word1) and \
           (result_word != word2) and \
           (result_word != word3):
           
            output_word = result_word
            break
        
    print(output_word)
    return output_word