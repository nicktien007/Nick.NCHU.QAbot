from serpapi import GoogleSearch

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
    answer = {"answer": "", "answerQty": 0, "result": {"A": 0, "B": 0, "C": 0}}

    for result in json_results["organic_results"]:
        # 考慮Title很容易出現最相關內容，故以2分計算，內容以1分計算
        answer["result"]["A"] += (result["title"].count(a) * 2)
        answer["result"]["A"] += (result["snippet"].count(a) * 1)
        answer["result"]["B"] += (result["title"].count(b) * 2)
        answer["result"]["B"] += (result["snippet"].count(b) * 1)
        answer["result"]["B"] += (result["title"].count(c) * 2)
        answer["result"]["B"] += (result["snippet"].count(c) * 1)

    # 計算得分最高的選項，因考量分數可能相同，故以 anserQty告知最高分有幾個
    highestScore = max(answer["result"].values())
    for j in answer["result"].values():
        if (highestScore == j):
            answer["answerQty"] += 1

    # 判斷考量若搜尋不到相關資料，顯示 none
    if (highestScore != 0):
        answer["answer"] = max(answer["result"], key=answer["result"].get)
    else:
        answer["answer"] = "none"

    return answer