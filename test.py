import codecs
import json
import operator
from collections import defaultdict, Counter
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
            dic[r1[0]] = list(map(lambda x: int(x), r1[1].split(',')))
    saveJson_writeline(dic, "./dataset/wiki_db_art_final_v2_j.json")
    # saveJson_writeline(dic,"./dataset/test_j.json")


def case_3():
    start = time.time()
    j = load_json("./dataset/wiki_db_art_final_v2_j.json")
    # j = load_json("./dataset/test_j.json")
    end = time.time()
    print('load = ', end - start)

    # # ok, 402
    ques_tokenized_1 = tokenize(
        "官方稱以色列國，是在位於西亞的主權國家，坐落於地中海東南岸及紅海亞喀巴灣北岸，北靠黎巴嫩，東北鄰敘利亞，東與約旦接壤，巴勒斯坦領土的約旦河西岸地區和加薩走廊各居東西，西南則為埃及。")
    ans_tokenized_1 = ["西班牙", "以色列", "孟加拉"]
    #
    # # ok
    ques_tokenized_2 = tokenize(
        "簡稱臺大，前身為日治時期1928年創立的臺北帝國大學，由首任校長幣原坦籌設，原初只定位為醫學和農學的實業大學，由時任總督伊澤多喜男改為籌設成綜合大學之目標。臺北帝國大學在二次大戰後二次改名，1945年11月易名為國立臺北大學，同年12月15日啟用現名國立臺灣大學，以自由主義學風著稱，是臺灣第一所現代綜合大學。")
    ans_tokenized_2 = ["國立高雄大學", "國立台南大學", "國立臺灣大學"]

    # ok,135
    ques_tokenized_3 = tokenize(
        "簡稱雲或滇，是中華人民共和國西南部邊疆地區的一個省份，省會昆明。雲南是人類重要的發祥地之一，生活在距今170萬年前的雲南元謀猿人，是迄今為止發現的中國乃至亞洲最早的人類。戰國時期，這裡是滇族部落的生息之地。")
    ans_tokenized_3 = ["魁北克省", "雲南省", "安大略省"]

    # # ok
    ques_tokenized_4 = tokenize(
        "或稱「高地綜合症、高山反應、高原反應」，是人體在高海拔狀態由於氧氣濃度降低而出現的急性病理變化表現。它通常出現在海拔2438公尺以上。可以發展成肺水腫和腦水腫，嚴重時可致死。")
    ans_tokenized_4 = ["亞斯伯格症", "高山症", "憂鬱症"]
    #
    # ok, 11
    ques_tokenized_5 = tokenize(
        "是日本戰國時代的大名及江戶幕府第一任征夷大將軍，全名德川次郎三郎源朝臣家康，為日本於1598年至1616年的實際元首，與其同時代的織田信長、豐臣秀吉並稱「戰國三傑」。")
    ans_tokenized_5 = ["德川家康", "小笠原道大", "村上春樹"]

    # # ok,140
    ques_tokenized_6 = tokenize(
        "是中華人民共和國西南地區的一個省份，省會成都市。四川簡稱川或蜀，又因先秦時四川曾分屬巴國、蜀國兩諸侯國，故別稱「巴蜀」。四川歷史悠久、風光秀麗、物產豐富，自古被譽為「天府之國」。")
    ans_tokenized_6 = ["四川省", "遼寧省", "河北省"]

    # ques_tokenized_7 = tokenize(
    #     "明末清初著名軍事將領，曾因「引清兵入關」而被世人斥責為漢奸，他的名字叫做:")
    # ans_tokenized_7 = ["吳一桂", "吳二桂", "吳三桂"]

    start_total = time.time()

    start = time.time()
    ans_dic = get_model_indexted_res(j, ans_tokenized_6)
    end = time.time()
    print('get ans_dic = ', end - start)
    if len(ans_dic.items()) == 1:
        print(ans_dic.keys())
        return

    start = time.time()
    ques_dic = get_model_indexted_res(j, ques_tokenized_6)
    end = time.time()
    print('get ques_dic = ', end - start)

    start = time.time()
    l_2 = []
    # ques_dic_values = list(ques_dic.values())
    # list(set(list1).intersection(set(list2),set(list3),....))
    # ll = set(ques_dic_values[0]).intersection(*ques_dic_values)
    #
    # print("ll=", ll)
    # result = set(lists[0]).intersection(*lists)
    for i in ques_dic.values():
        l_2 += i

    quest_counter = {x: count for x, count in Counter(l_2).items()}

    answer = calc_ans(quest_counter, ans_dic)
    end = time.time()
    print('get answer = ', end - start)

    end_total = time.time()
    print('run_time = ', end_total - start_total)
    print(answer)


def process_tokenized(tokenized):
    j = load_json("./dataset/wiki_db_wordcount_j.json")
    res = {}
    for t in tokenized:
        if t in j:
            res[t] = j[t]
    return sorted(res.items(), reverse=True, key=lambda x: x[1])[:10]


def process_wiki_db_wordcount():
    dic = {}
    with open("./dataset/wiki_db_wordcount.txt", 'r', encoding='utf-8') as file:
        for line in file:
            r1 = line.replace("\n", "").split(' ')
            dic[r1[0]] = int(r1[1])
        saveJson_writeline(dic, "./dataset/wiki_db_wordcount_j.json")


def get_model_indexted_res(j, tokenized):
    res_dic = {}
    for key in tokenized:
        if key in j:
            res_dic[key] = j[key]

    return res_dic


def case_4():
    tokenized = tokenize(
        "簡稱雲或滇，是中華人民共和國西南部邊疆地區的一個省份，省會昆明。雲南是人類重要的發祥地之一，生活在距今170萬年前的雲南元謀猿人，是迄今為止發現的中國乃至亞洲最早的人類。戰國時期，這裡是滇族部落的生息之地。")
    print(tokenized)


def tokenized(sentence):
    return tokenize(sentence)


def calc_ans(ll, ans_dic):
    score_dic = {}
    score = 0
    # ll = []
    #
    # for l in ques_dic.values():
    #     ll+=l

    for a in ans_dic.items():
        start = time.time()
        for input_v in a[1]:
            score += get_score_of_inputV(input_v, ll)
        end = time.time()
        print("get_score_of_inputV time = ", end - start)
        print(a[0], 'score_tal=', str(score))
        score_dic[a[0]] = score
        score = 0
    return max(score_dic.items(), key=operator.itemgetter(1))[0]


def get_score_of_inputV(input_v, ll):
    score = 0
    # ll=[]
    # for ques_tuple in ques_dic.values():
    # ques_vals = ques_tuple[1]
    # ques_vals = ques_tuple
    # ll+=ques_tuple
    # r = list(ques_vals, filter(lambda x: x == v, ques_vals))
    # r = list(filter(lambda x: x == input_v, ques_vals))
    # score +=len(r)
    # score += len(list(filter(lambda x: x == input_v, ques_vals)))
    # print(score)
    # print(sum(r))
    # return len(set(filter(lambda x: x == input_v, ll)))
    # print(len(ll))

    # for v in ll:
    #     if input_v == v:
    #         score += 1
    if input_v in ll:
        # return 1
        return ll[input_v]

    return 0
    # print('input_v=', input_v, 'score=', score)


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


def case_6():
    lists = [[1, 4, 7], [4, 5, 8], [4, 8, 0]]
    retB = []
    result = set(lists[0]).intersection(*lists)
    print(result)
    # for i in range(len(lists)-3):
    #     retB += list(set(first).intersection(set(lists[i+1])))
    # print(retB)


def main():
    # case_2()
    case_3()
    # case_4()
    # case_5()
    # case_6()
    # process_wiki_db_wordcount()
    # process_tokenized(['簡稱', '雲', '滇', '中華人民共和國', '西南部', '邊疆地區', '一個', '省份', '省會', '昆明', '雲南', '人類', '重要', '發祥地', '生活', '距今', '170', '萬年前', '雲南', '元謀猿人', '迄今', '為止', '發現', '中國', '亞洲', '最早', '人類', '戰國時期', '滇', '族', '部落', '生息'])


if __name__ == '__main__':
    main()
