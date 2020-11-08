from collections import defaultdict
from file_utils import saveJson


def pre_process_wiki_db(wiki_path, output_path):
    dic = defaultdict(set)

    with open(wiki_path, 'r', encoding='utf-8') as file:
        for line in file:
            r1 = line.replace("\n", "").split('|')
            dic[r1[0]] = list(map(lambda x: int(x), r1[1].split(',')))
    saveJson(dic, output_path)


def pre_process_wiki_db_wordcount():
    # 暫時沒有用
    dic = {}
    with open("./dataset/wiki_db_wordcount.txt", 'r', encoding='utf-8') as file:
        for line in file:
            r1 = line.replace("\n", "").split(' ')
            dic[r1[0]] = int(r1[1])
        saveJson(dic, "./dataset/wiki_db_wordcount_j.json")
