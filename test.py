import json
import time
from collections import defaultdict

from enums.answer_type import AnswerType
from service.calc_score_service import start_QA_bot, calc_ABC, get_ans_index_val_score, build_idx_answers, filter_ans_by
from service.tokenize_service import tokenize
from utils.file_utils import load_json
from thirdparty.google import googleApi

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
    print('load model...')
    start = time.time()
    wiki = load_json("./dataset/wiki_db_art_final_v2_j.json")
    # j = load_json("./dataset/test_j.json")
    end = time.time()
    print('load = ', end - start)

    ques_tokenized = tokenize(
        (0, "《笑傲江湖》是金庸寫的武俠小說，小說男主角令狐沖於思過崖習得何種劍法?"))
    ques = "下列哪個顏色存在奧林匹克五環中出現"
    ans_tokenized = ["黃色", "橙色", "粉色"]

    start_total = time.time()
    res = calc_ABC(wiki, (0,ques), ans_tokenized)
    end_total = time.time()

    google_res = googleApi(ques,ans_tokenized[0],ans_tokenized[1],ans_tokenized[2])

    print(res[0])
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


def test_find_filter_answers():
    ans = [("B", 1), ("C", 3), ("B", 2), ("A", 4), ("B", 1), ("A", 2), ("A", 3), ("C", 2), ("B", 1), ("B", 2), ("C", 3),
           ("A", 4), ("B", 1)]
    print("NOT_FOUND:", filter_ans_by(AnswerType.NOT_FOUND, ans))
    print("ONLY_ONE:", filter_ans_by(AnswerType.ONLY_ONE, ans))
    print("MANUAL:", filter_ans_by(AnswerType.MANUAL, ans))

    indexes, results = build_idx_answers(map(lambda x: x[0], ans))

    for i, v in enumerate(indexes):
        print(v)
        print(results[i])
        print()


def test_merage_answer():
    j = load_json("./dataset/merage_answer.json")
    ans_4 = []
    ans_4 += map(lambda x: str(x).strip(), j["nick"])
    ans_4 += map(lambda x: str(x).strip(), j["sunny"])
    ans_4 += map(lambda x: str(x).strip(), j["學長"])
    ans_4 += map(lambda x: str(x).strip(), j["建德"])

    print(json.dumps(ans_4))


def test_google_api():
    question = "小說《絕代雙驕》中，主角江小魚又稱小魚兒，請問何人為其兄弟?"
    answer1 = "大魚兒"
    answer2 = "江大魚"
    answer3 = "花無缺"

    answer = googleApi(question, answer1, answer2, answer3)

    print(answer)


def main():
    # pre_process_wiki_db()
    # pre_process_wiki_db_wordcount()
    test_one_calc_score()
    # test_start_QA_bot()
    # test_tokenize()
    # case_5()
    # case_6()
    # data_utils.download_data_gdown("./dataset/")
    # print(extract_tags("世界衛生組織"))
    # test_ckip()
    # test_show_answers()
    # val_answers()
    # test_find_filter_answers()
    # test_merage_answer()
    # test_google_api()


def test_show_answers():
    lists = ["B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B",
             "B", "A", "B", "B", "A", "A", "C", "A", "A", "B", "B", "B", "B", "C", "A", "A", "B", "A", "C", "B"]
    indexes, results = build_idx_answers(lists)

    for i, v in enumerate(indexes):
        print(v)
        print(results[i])
        print()


if __name__ == '__main__':
    main()
