import time
from collections import defaultdict

from service.calc_score_service import start_QA_bot, calc_ABC, get_ans_index_val_score, build_idx_answers
from service.tokenize_service import tokenize
from utils.file_utils import load_json


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
    print(i.search('july'))


def test_one_calc_score():
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
    ans_tokenized_2 = ["高雄大學", "台南大學", "臺灣大學"]
    # ans_tokenized_2 = ckip(["國立高雄大學", "國立台南大學", "國立臺灣大學"])

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

    ques_tokenized_7 = tokenize(
        (0, "《笑傲江湖》是金庸寫的武俠小說，小說男主角令狐沖於思過崖習得何種劍法?"))
    ans_tokenized_7 = ["天外飛仙", "獨孤九劍", "破雲摘星九九八十一劍"]

    ques_tokenized_8 = tokenize(
        "是一個由主權國家組成的國際組織，致力於促進各國在國際法、國際安全、經濟發展、社會進步、人權、公民自由、政治自由、民主及實現持久世界和平方面的合作。成立於第二次世界大戰結束後的1945年，取代國際聯盟以阻止戰爭並為各國提供對話平臺。")
    ans_tokenized_8 = ["貿易", "聯合國", "衛生"]
    # ans_tokenized_8 = ["世界貿易組織", "聯合國", "世界衛生組織"]

    start_total = time.time()
    calc_ABC(j, ques_tokenized_7, ans_tokenized_7)
    end_total = time.time()
    print('run_time = ', end_total - start_total)


def test_start_QA_bot():
    wiki_path = "./dataset/wiki_db_art_final_v2_j.json"
    question_path = "./dataset/question.json"
    answers = start_QA_bot(wiki_path, question_path)
    print(answers)


def test_tokenize():
    tokenized = tokenize(
        "聯合國")
    print(tokenized)


def case_5():
    ques_dic = {"吳一桂": [1, 4, 6, 7, 88],
                "吳二桂": [1, 88, 3, 7, 77],
                "吳三桂": [1, 99]}

    ans_dic = {"A": [99, 44],
               "B": [14, 33, 88, 77]}

    score_dic = {}
    score = 0
    for a in ans_dic.items():
        for input_v in a[1]:
            score += get_ans_index_val_score(input_v, ques_dic)
        print(a[0], 'score_tal=', str(score))
        score_dic[a[0]] = score
        score = 0


def case_6():
    lists = [[1, 4, 7], [4, 5, 8], [4, 8, 0]]
    result = set(lists[0]).intersection(*lists)
    print(result)


def print_word_pos_sentence(word_sentence, pos_sentence):
    assert len(word_sentence) == len(pos_sentence)
    for word, pos in zip(word_sentence, pos_sentence):
        print(f"{word}({pos})", end="\u3000")
    print()
    return


def val_answers():
    ans = ["B", "C", "B", "A", "B", "A", "A", "C", "B", "B", "C", "A", "B", "B", "A", "B", "A", "C", "B", "B", "C", "A",
           "C", "A", "A", "C", "B", "B", "A", "B", "C", "A", "C", "C", "A", "B", "A", "C", "B", "A", "B", "C", "A", "B",
           "A", "C", "A", "B", "A", "C", "C", "B", "A", "C", "A", "B", "B", "C", "B", "B", "B", "B", "B", "C", "C", "B",
           "B", "C", "B", "B", "A", "B", "B", "C", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B", "B", "C",
           "A", "C", "C", "C", "A", "A", "B", "A", "A", "C", "B", "C", "C", "C", "B", "B", "A", "A", "C", "C", "B", "A",
           "C", "B", "C", "B", "A", "A", "A", "C", "B", "C", "A", "A", "A", "C", "C", "A", "B", "A", "B", "A", "B", "B",
           "B", "C", "C", "B", "A", "B", "C", "A", "A", "C", "A", "A", "B", "C", "B", "A", "A", "B", "A", "A", "B", "A",
           "A", "A", "A", "B", "C", "A", "A", "B", "A", "C", "A", "A", "A", "A", "C", "A", "C", "C", "A", "C", "A", "C",
           "B", "C", "A", "A", "A", "C", "B", "A", "C", "A", "A", "A", "B", "B", "B", "A", "C", "A", "A", "B", "B", "B",
           "B", "B"]
    j = load_json("./dataset/Questions_with_Ans.json")
    aa = list(map(lambda x: (x["Answer"]), j))
    count = 0
    for i, a in enumerate(aa):
        if list(aa)[i] != ans[i]:
            count += 1
    print(count)


def main():
    # pre_process_wiki_db()
    # pre_process_wiki_db_wordcount()
    # test_one_calc_score()
    # test_start_QA_bot()
    # test_tokenize()
    # case_5()
    # case_6()
    # data_utils.download_data_gdown("./dataset/")
    # print(extract_tags("世界衛生組織"))
    # test_ckip()
    test_show_answers()
    # val_answers()



def test_show_answers():
    lists = ["B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B","A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A","B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B","B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B","A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A","A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A","C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C","A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A","A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B"]
    indexes, results = build_idx_answers(lists)

    for i,v in enumerate(indexes):
        print(v)
        print(results[i])
        print()


if __name__ == '__main__':
    main()
