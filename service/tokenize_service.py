import codecs
import jieba
import jieba.posseg as psg
import jieba.analyse



# from opencc import OpenCC
from ckiptagger import WS, POS, NER

jieba.set_dictionary('./dict/dict.txt.big.txt')
# cc = OpenCC('s2t')  # s2t: 簡體中文 -> 繁體中文


# 中文斷詞
def tokenize(sentence):
    stopword_set = get_stopword_set()

    # converted = cc.convert(sentence)  # 簡>繁
    words = jieba.posseg.cut(sentence)
    words = [w.word for w in words if w.word not in stopword_set]
    print(words)
    return words


def get_stopword_set():
    stopword_set = set()
    with codecs.open('../dict/stopwords.txt', 'r', 'utf-8') as stopwords:
        for stopword in stopwords:
            stopword_set.add(stopword.strip('\n'))
    return stopword_set


def extract_tags(sentence):
    return jieba.analyse.textrank(sentence, topK=20, withWeight=False, allowPOS=())
    # return jieba.analyse.extract_tags(sentence, topK=10)

def ckip(sentences):
    ws = WS("../dataset/data")
    pos = POS("../dataset/data")
    ner = NER("../dataset/data")

    sentence_list = [
        # "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
        # "美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
        # "",
        # "土地公有政策?？還是土地婆有政策。.",
        # "… 你確定嗎… 不要再騙了……",
        # "最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.",
        # "科長說:1,坪數對人數為1:3。2,可以再增加。",
        # "世界貿易組織",
        # "聯合國",
        # "世界衛生組織",
        # "國立高雄大學",
        # "國立台南大學",
        # "國立臺灣大學"
        # sentence
    ]

    word_sentence_list = ws(
        # sentence_list,
        sentences
        # sentence_segmentation = True, # To consider delimiters
        # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
        # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
        # coerce_dictionary = dictionary2, # words in this dictionary are forced
    )

    pos_sentence_list = pos(word_sentence_list)

    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    r = []
    for i, sentence in enumerate(sentences):
        for entity in sorted(entity_sentence_list[i]):
            # print("================",entity)
            r.append(entity[3])
            print("================", entity[3])

    return r


# def ckiptagger_