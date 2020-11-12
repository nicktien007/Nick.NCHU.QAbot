# Unit testing
import unittest

# Operating system
import os

# regular expression library
import re

# safe queue
import sys

from queue import Queue

# Time utility
import time

# Serp API search
from serpapi import GoogleSearch


# download file with wget
# import wget

def setUp():
    # GoogleSearch.SERP_API_KEY = os.getenv("API_KEY", "demo")
    GoogleSearch.SERP_API_KEY = "ecf62f54c84522b61d763db639364ada706243bdefcd988bfb9f53ab472d4d68"


def test_async():
    # store searches
    search_queue = Queue()

    # Serp API search
    search = GoogleSearch({
        "location": "Austin,Texas",
        "async": True
    })

    # loop through companies
    for company in ['官方稱以色列國，是在位於西亞的主權國家，坐落於地中海東南岸及紅海亞喀巴灣北岸，北靠黎巴嫩，東北鄰敘利亞，東與約旦接壤，巴勒斯坦領土的約旦河西岸地區和加薩走廊各居東西，西南則為埃及。',
                    '簡稱臺大，前身為日治時期1928年創立的臺北帝國大學，由首任校長幣原坦籌設，原初只定位為醫學和農學的實業大學，由時任總督伊澤多喜男改為籌設成綜合大學之目標。臺北帝國大學在二次大戰後二次改名，1945年11月易名為國立臺北大學，同年12月15日啟用現名國立臺灣大學，以自由主義學風著稱，是臺灣第一所現代綜合大學。',
                    '簡稱雲或滇，是中華人民共和國西南部邊疆地區的一個省份，省會昆明。雲南是人類重要的發祥地之一，生活在距今170萬年前的雲南元謀猿人，是迄今為止發現的中國乃至亞洲最早的人類。戰國時期，這裡是滇族部落的生息之地。']:
        print("execute async search: q = " + company)
        search.params_dict["q"] = company
        data = search.get_dict()
        print("add search to the queue where id: " + data['search_metadata']['id'])
        # add search to the search_queue
        search_queue.put(data)

    print("wait until all search statuses are cached or success")

    # Create regular search
    search = GoogleSearch({"async": True})
    while not search_queue.empty():
        data = search_queue.get()
        search_id = data['search_metadata']['id']

        # retrieve search from the archive - blocker
        print(search_id + ": get search from archive")
        search_archived = search.get_search_archive(search_id)
        print(search_id + ": status = " + search_archived['search_metadata']['status'])

        # check status
        if re.search('Cached|Success', search_archived['search_metadata']['status']):
            print(search_id + ": search done with q = " + search_archived['search_parameters']['q'])
        else:
            # requeue search_queue
            print(search_id + ": requeue search")
            search_queue.put(search)
            # wait 1s
            time.sleep(1)
    # search is over.
    print('all searches completed')






if __name__ == '__main__':
    setUp()
    test_async()