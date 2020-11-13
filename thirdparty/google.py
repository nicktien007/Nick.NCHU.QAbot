# -*- coding: utf-8 -*-
from asyncio import Queue

from serpapi import GoogleSearch
# regular expression library
import re

# safe queue
import sys

from queue import Queue

# Time utility
import time

from utils.file_utils import load_json

QUERY_RESULT = {}


def search(keyword):
    # 在這邊寫入查詢程式碼，先查前五筆資料
    pass


def setUp():
    # GoogleSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
    GoogleSearch.SERP_API_KEY = "ecf62f54c84522b61d763db639364ada706243bdefcd988bfb9f53ab472d4d68"


def googleApi(question, a, b, c):
    """
    search = GoogleSearch({})
    location_list = search.get_location("Austin", 3)
    print(location_list)
    """

    search = build_search(question)
    search.params_dict["q"] = question

    return calc(search.get_json(), a, b, c)


def search_QUERY_RESULT(question, a, b, c, wiki_answer="C"):
    key = question[-5:]
    if key in QUERY_RESULT:
        return calc(QUERY_RESULT[key], a, b, c)
    # google答案 就回傳 傳入的 wiki_answer
    return wiki_answer


def calc(organic_results, a, b, c):
    # 結果 answer:答案選項、answerQty:最高分有幾個、result:各選項分數
    answer = {"answer": "",
              "answerQty": 0,
              "result": {"A": 0, "B": 0, "C": 0}}

    # snippets = []
    for result in organic_results:
        # 考慮Title很容易出現最相關內容，故以2分計算，內容以1分計算
        answer["result"]["A"] += (result["title"].count(a) * 2)
        answer["result"]["B"] += (result["title"].count(b) * 2)
        answer["result"]["C"] += (result["title"].count(c) * 2)
        if "snippet" in result:
            answer["result"]["A"] += (result["snippet"].count(a) * 1)
            answer["result"]["B"] += (result["snippet"].count(b) * 1)
            answer["result"]["C"] += (result["snippet"].count(c) * 1)

        # snippets.append(result["snippet"][:30]+"...")

    # answer["googleResult"] = snippets

    # 計算得分最高的選項，因考量分數可能相同，故以 anserQty告知最高分有幾個
    highestScore = max(answer["result"].values())
    for j in answer["result"].values():
        if (highestScore == j):
            answer["answerQty"] += 1

    # 判斷考量若搜尋不到相關資料，顯示 C
    if (highestScore != 0):
        answer["answer"] = max(answer["result"], key=answer["result"].get)
    else:
        answer["answer"] = "C"

    return answer


def build_search(is_async=False):
    params = {
        # "q": question,
        "location": "Austin, TX",
        "device": "desktop",
        "hl": "zh-tw",
        "gl": "tw",
        "safe": "active",  # active, or off
        "num": "10",
        "start": "0",
        "api_key": "ecf62f54c84522b61d763db639364ada706243bdefcd988bfb9f53ab472d4d68",
        # To be match
        # "tbm": "nws|isch|shop", #use default
        # To be search
        # "tbs": "custom to be search criteria", #use default
        # allow async request
        "async": is_async,
        # output format
        "output": "json"
    }
    return GoogleSearch(params)


def search_async(ques_path, show_msg=False):
    # store searches
    setUp()
    print("Start Search_async...")
    search_queue = Queue()
    search = build_search(is_async=True)

    json_q = load_json(ques_path)

    q_list = list(map(lambda x: x["Question"], json_q))

    # loop through companies
    for q in q_list:
        search.params_dict["q"] = q
        data = search.get_dict()

        # add search to the search_queue
        search_queue.put(data)

        if show_msg:
            print("execute async search: q = " + q)
            print("add search to the queue where id: " + data['search_metadata']['id'])

    print("wait until all search statuses are cached or success")

    # Create regular search
    search = GoogleSearch({"async": True})
    while not search_queue.empty():
        data = search_queue.get()
        search_id = data['search_metadata']['id']

        # retrieve search from the archive - blocker
        search_archived = search.get_search_archive(search_id)
        if show_msg:
            print(search_id + ": get search from archive")
            print(search_id + ": status = " + search_archived['search_metadata']['status'])

        # check status
        if re.search('Cached|Success', search_archived['search_metadata']['status']):
            if show_msg:
                print(search_id + ": search done with q = " + search_archived['search_parameters']['q'])
            QUERY_RESULT[search_archived['search_parameters']['q'][-5:]] = search_archived["organic_results"]
        else:
            # requeue search_queue
            print(search_id + ": requeue search")
            search_queue.put(search)
            # wait 1s
            time.sleep(1)
    # search is over.
    print('all searches completed')

def main():
    """
    question = "中華民國第14任總統，民主進步黨第16屆黨主席，同時也是台灣歷史上首位女性元首，她是:"
    answer1 = "蔡正元"
    answer2 = "蔡英文"
    answer3 = "洪慈庸"
    """
    question = "小說《絕代雙驕》中，主角江小魚又稱小魚兒，請問何人為其兄弟?"
    answer1 = "大魚兒"
    answer2 = "江大魚"
    answer3 = "花無缺"

    answer = googleApi(question, answer1, answer2, answer3)

    print(answer)


if __name__ == "__main__":
    main()
    # search_async()
