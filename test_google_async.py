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
from utils.file_utils import load_json


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

    json_q = load_json("./dataset/Questions_with_Ans.json")
    # json_q = load_json("./dataset/question.json")

    ll = list(map(lambda x: x["Question"], json_q))

    # loop through companies
    for company in ll:
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
            print(search_archived["organic_results"])
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