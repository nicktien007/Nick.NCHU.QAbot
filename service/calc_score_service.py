import json
import operator
import time
from collections import Counter

from enums.answer_type import AnswerType
from thirdparty.google import googleApi, search_QUERY_RESULT
from utils.file_utils import load_json
from service.tokenize_service import tokenize


def start_QA_bot(wiki_path, question_path):
    print('load model...')
    start = time.time()
    wiki_db_json = load_json(wiki_path)
    question = load_json(question_path)
    end = time.time()
    print('load time = ', end - start)

    return start_QA_bot_input_json(wiki_db_json, question)


def start_QA_bot_input_json(wiki_db_json, question_json):
    start_total = time.time()
    answers = [calc_ABC(wiki_db_json,
                        (i, q["Question"]),
                        [q["A"], q["B"], q["C"]])
               for i, q in enumerate(question_json)]
    end_total = time.time()
    print('run_time = ', end_total - start_total)
    print("人工比對:", filter_ans_by(AnswerType.MANUAL, answers))
    print("找不到答案:", filter_ans_by(AnswerType.NOT_FOUND, answers))
    print("只找到一個:", filter_ans_by(AnswerType.ONLY_ONE, answers))
    show_answers_by_chunk(list(map(lambda x: x[0], answers)))
    print("==================================================")
    return json.dumps(list(map(lambda x: x[0], answers)))


def show_answers_by_chunk(answers):
    chunks_index, chunks_result = build_idx_answers(answers)

    for i, v in enumerate(chunks_index):
        if i == 0:
            print("nick:")
        elif i == 1:
            print("sunny:")
        elif i == 2:
            print("學長:")
        elif i == 3:
            print("建德:")

        print(json.dumps(v))
        print(json.dumps(chunks_result[i]))
        print()


def calc_ABC(wiki_db_json, question_info, ansers):
    """
    計算答案A、B、C及狀態
    :param wiki_db_json:
    :param question_info:[0]=>index, [1]=>question
    :param ansers:
    :return: [0]=>A、B、C , [1]=>AnswerTypeEnum
    """
    ans_index = get_tokenized_indexted(wiki_db_json, ansers)
    ques_tokenized = tokenize(question_info)

    if len(ans_index.keys()) == 0:
        print(ansers)
        print("********** 找不到答案，調用GoogleSearch ***********\n")
        # google_res = googleApi(question_info[1], ansers[0], ansers[1], ansers[2])
        google_res = search_QUERY_RESULT(question_info[1], ansers[0], ansers[1], ansers[2])
        answer_abc = google_res["answer"]
        print("=====GOOGLG 的建議:", "(", answer_abc, ")", google_res, "=====", end="\n\n")
        return answer_abc, AnswerType.NOT_FOUND

    # 如果只有一個答案在wiki找到，直接回傳該答案就好
    if len(ans_index.keys()) == 1:
        print(ansers)
        print("############只找到一個答案############")
        answer_abc = to_ABC(list(ans_index.keys())[0], ansers)
        print("=====(", answer_abc, ")", list(ans_index.keys())[0], "=====", end="\n\n")
        return answer_abc, AnswerType.ONLY_ONE

    ques_index = get_tokenized_indexted(wiki_db_json, ques_tokenized)
    quest_counter = to_quest_counter(ques_index)

    answer = calc_ans(quest_counter, ans_index)
    ans_abc = to_ABC(answer, ansers)

    google_res = search_QUERY_RESULT(question_info[1], ansers[0], ansers[1], ansers[2], wiki_answer=ans_abc)

    if ans_abc != google_res["answer"]:
        print(ansers)
        print("===== WIKI  的答案:", ans_abc, "=====", end="\n")
        print("=====GOOGLG 的建議:", google_res["answer"], "=====", end="\n\n")
        return google_res["answer"], AnswerType.MANUAL

    print(ansers)
    print("=====(", ans_abc, ")", answer, "=====", end="\n\n")
    return ans_abc, AnswerType.OK


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
        print(a[0], 'score =', score_avg)

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


def build_idx_answers(lists, chunk_siz=50):
    index = []
    result = []
    for i, v in enumerate(lists):
        input_s = to_formatter(i, v)
        result.append(input_s)
        index.append(str(i))

    chunks_index = [index[x:x + chunk_siz] for x in range(0, len(index), chunk_siz)]
    chunks_result = [result[x:x + chunk_siz] for x in range(0, len(result), chunk_siz)]

    return chunks_index, chunks_result


def to_formatter(index, val):
    if len(str(index)) == 1:
        input_s = "%s" % str(val)
    elif len(str(index)) == 2:
        input_s = "%s " % str(val)
    else:
        input_s = "%s  " % str(val)
    return input_s


def filter_ans_by(answer_type, ans):
    """
    回傳答案 by answer_type
    :param answer_type: AnswerType
    :param ans:
    :return: [2,5,7,9]
    """
    return list(map(lambda y: y[0], filter(lambda x: x[1][1] == answer_type, enumerate(ans))))
    # return list(filter(lambda x: x[1][1] == answer_type, enumerate(ans)))
