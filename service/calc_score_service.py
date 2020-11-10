import json
import operator
import time
from collections import Counter
from utils.file_utils import load_json
from service.tokenize_service import tokenize


def start_QA_bot(wiki_path, question_path):
    start = time.time()
    wiki_db_json = load_json(wiki_path)
    question = load_json(question_path)
    end = time.time()
    print('load = ', end - start)

    start_total = time.time()
    answers = [calc_ABC(wiki_db_json, tokenize(q["Question"]), [q["A"], q["B"], q["C"]]) for q in question]
    end_total = time.time()
    print('run_time = ', end_total - start_total)
    return json.dumps(answers)


def calc_ABC(wiki_db_json, ques_tokenized, ans_tokenized):
    ans_index = get_tokenized_indexted(wiki_db_json, ans_tokenized)

    # 如果只有一個答案在wiki找到，直接回傳該答案就好
    if len(ans_index.keys()) == 1:
        print(ans_index.keys())
        return to_ABC(list(ans_index.keys())[0], ans_tokenized)

    ques_index = get_tokenized_indexted(wiki_db_json, ques_tokenized)
    quest_counter = to_quest_counter(ques_index)

    answer = calc_ans(quest_counter, ans_index)
    print("===", answer, "===", end="\n\n")

    return to_ABC(answer, ans_tokenized)


def get_tokenized_indexted(wiki_db_json, tokenized):
    """
    從 wiki_db 取得tokenized的索引
    :param wiki_db_json:
    :param tokenized:
    :return: index dictionary

    {"A":[22,33,55],
    "B":[777,88,1243,39]
    "C":[44,20]}
    """
    res_dic = {}
    for key in tokenized:
        if key in wiki_db_json:
            res_dic[key] = wiki_db_json[key]
    return res_dic


def to_quest_counter(ques_index):
    """
    將問題集的索引先合併到一個集合，然後使用 Counter進行group by 加總
    :param ques_index:
    :return: group by dictionary

    [3,5,7,9,3,5,5] => {3:2,5:3,7:1,9:1}
    """
    all_ques_index = []
    for i in ques_index.values():
        all_ques_index += i

    return {x: count for x, count in Counter(all_ques_index).items()}


def calc_ans(quest_counter, ans_index):
    """
    計算 答案
    :param quest_counter: 答案index group by 集合
    :param ans_index: A、B、C 三個選項的Index 集合
    :return: 答案 (不是回傳ABC)
    """
    score_dic = {}

    for a in ans_index.items():
        score = 0
        for ans_index_val in a[1]:
            score += get_ans_index_val_score(ans_index_val, quest_counter)

        score_avg = score / len(a[1])  # 取平均
        score_dic[a[0]] = score_avg
        print(a[0], 'score_tal=', score_avg)

    return max(score_dic.items(), key=operator.itemgetter(1))[0]


def get_ans_index_val_score(ans_index_val, quest_counter):
    return quest_counter[ans_index_val] if ans_index_val in quest_counter else 0


def to_ABC(answer, ans_tokenized):
    if list(ans_tokenized).__contains__(answer):
        ans_tokenized_idx = ans_tokenized.index(answer)
        if ans_tokenized_idx == 0:
            return "A"
        elif ans_tokenized_idx == 1:
            return "B"
    return "C"
