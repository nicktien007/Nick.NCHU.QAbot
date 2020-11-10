import codecs
import jieba
import jieba.posseg as psg
import jieba.analyse

# from opencc import OpenCC

jieba.set_dictionary('dict/dict.txt.big.txt')


# cc = OpenCC('s2t')  # s2t: 簡體中文 -> 繁體中文


# 中文斷詞
def tokenize(sentence_info):
    stopword_set = get_stopword_set()
    index = sentence_info[0]
    sentence = sentence_info[1]
    print(str(index) + "." + sentence)

    # converted = cc.convert(sentence)  # 簡>繁
    words = jieba.posseg.cut(sentence)
    words = [w.word for w in words if w.word not in stopword_set]
    # print(words)
    return words


def get_stopword_set():
    stopword_set = set()
    with codecs.open('dict/stopwords.txt', 'r', 'utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))
    return stopword_set


def extract_tags(sentence):
    return jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=())
    # return jieba.analyse.extract_tags(sentence, topK=10)
