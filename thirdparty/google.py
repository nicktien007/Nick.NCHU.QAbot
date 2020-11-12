# -*- coding: utf-8 -*-
from serpapi import GoogleSearch


def search(keyword):
    # 在這邊寫入查詢程式碼，先查前五筆資料nick,nick
    pass


def googleApi(question, a, b, c):
    """
    search = GoogleSearch({})
    location_list = search.get_location("Austin", 3)
    print(location_list)
    """

    params = {
        "q": question,
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
        # "async": "true|false",
        # output format
        "output": "json"
    }

    search = GoogleSearch(params)
    json_results = search.get_json()

    # 結果 answer:答案選項、answerQty:最高分有幾個、result:各選項分數
    answer = {"answer": "",
              "answerQty": 0,
              "result": {"A": 0, "B": 0, "C": 0}}

    # snippets = []
    for result in json_results["organic_results"]:
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
