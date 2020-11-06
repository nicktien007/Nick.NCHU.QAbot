import codecs
import json
import operator
from collections import defaultdict
import time
from itertools import groupby
from operator import itemgetter

from tokenize_service import tokenize


class inverted_index:
    def __init__(self, docs):
        self.doc = defaultdict(set)
        for index, doc in enumerate(docs):
            for term in doc.split():
                self.doc[term].add(index)

    def search(self, term):
        return self.doc[term]


def case_1():
    docs = ["new home sales top forecasts june june june",
            "home sales rise in july june",
            "increase in home sales in july",
            "july new home sales new rise"]

    i = inverted_index(docs)
    a = 1
    print(i.search('july'))


def saveJson_writeline(data, file_path):
    with codecs.open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=lambda x: x.__dict__)


def load_json(file_path):
    with open(file_path, mode="r") as file:
        return json.load(file)


def case_2():
    dic = defaultdict(set)

    with open("./dataset/wiki_db_art_final_v1.txt", 'r', encoding='utf-8') as file:
        # with open("./dataset/test.txt", 'r', encoding='utf-8') as file:
        for line in file:
            r1 = line.replace("\n", "").split('|')
            dic[r1[0]] = r1[1].split(',')
    saveJson_writeline(dic, "./dataset/wiki_db_art_final_v1_j.json")
    # saveJson_writeline(dic,"./dataset/test_j.json")


def case_3():
    j = load_json("./dataset/wiki_db_art_final_v1_j.json")
    # j = load_json("./dataset/test_j.json")

    ques_tokenized = tokenize("明末清初著名軍事將領，曾因「引清兵入關」而被世人斥責為漢奸，他的名字叫做:")
    # ques_tokenized = tokenize("中華民國第14任總統，民主進步黨第16屆黨主席，同時也是台灣歷史上首位女性元首，她是:")

    ans_tokenized = ["吳三桂", "吳二桂", "吳一桂"]
    # ans_tokenized = ["蔡正元", "蔡英文", "洪慈庸"]

    start = time.time()
    ques_dic = get_model_indexted_res(j, ques_tokenized)
    if len(ques_dic.items()) == 1:
        print(ques_dic.items()[0])
        return

    ans_dic = get_model_indexted_res(j, ans_tokenized)
    answer = calc_ans(ques_dic, ans_dic)
    end = time.time()
    print('run_time = ', end - start)
    print(answer)


def get_model_indexted_res(j, tokenized):
    res_dic = {}
    for key in tokenized:
        if key in j:
            res_dic[key] = j[key]

    return res_dic


def case_4():
    tokenized = tokenize("明末清初著名軍事將領，曾因「引清兵入關」而被世人斥責為漢奸，他的名字叫做:")
    print(tokenized)


def tokenized(sentence):
    return tokenize(sentence)


def calc_ans(ques_dic, ans_dic):
    score_dic = {}
    score = 0
    for a in ans_dic.items():
        for input_v in a[1]:
            score += get_score_of_inputV(input_v, ques_dic)
        print(a[0], 'score_tal=', str(score))
        score_dic[a[0]] = score
        score = 0
    score_dic.values()
    return max(score_dic.items(), key=operator.itemgetter(1))[0]


def case_5():
    # d_1 = {"吳一桂": [1, 4, 6, 7, 88]}
    # d_2 = {"吳二桂": [1, 88, 3, 7, 77]}
    # d_3 = {"吳三桂": [1, 99]}
    # d_list = [d_1, d_2, d_3]
    #
    # ans_a = {"A": [99, 44]}
    # ans_b = {"B": [14, 33, 88, 77]}
    # ans_list = [ans_a, ans_b]

    ques_dic = {"吳一桂": [1, 4, 6, 7, 88],
                "吳二桂": [1, 88, 3, 7, 77],
                "吳三桂": [1, 99]}

    ans_dic = {"A": [99, 44],
               "B": [14, 33, 88, 77]}

    score_dic = {}
    score = 0
    for a in ans_dic.items():
        for input_v in a[1]:
            score += get_score_of_inputV(input_v, ques_dic)
        print(a[0], 'score_tal=', str(score))
        score_dic[a[0]] = score
        score = 0

    # score_dic = {}
    # for a in ans_list:
    #     for v_list in a.values():
    #         for v in v_list:
    #             score += get_score_of_inputV(v, d_list)
    #         print(a, 'score_tal=', str(score))
    #         score_dic[v_list] = score
    #         score = 0


def get_score_of_inputV(input_v, d_dic):
    score = 0
    for items in d_dic.items():
        for v in items[1]:
            if input_v == v:
                score += 1

    return score
    print('input_v=', input_v, 'score=', score)


def main():
    # case_2()
    case_3()
    # case_4()
    # case_5()


if __name__ == '__main__':
    main()
