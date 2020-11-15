import time

from thread_with_return_value import ThreadWithReturnValue
from thirdparty.google import setUp, search_async
from utils import arg_parser_factory
from service.calc_score_service import start_QA_bot_input_json
from service.pre_process_service import pre_process_wiki_db
from utils.file_utils import load_json


def init_QA_bot(ques_path, wiki_path):
    # store searches
    setUp()
    print("Start Search_async...")

    json_q = load_json(ques_path)

    q_list = list(map(lambda x: x["Question"], json_q))
    q_split = [q_list[:50], q_list[50:100], q_list[100:150], q_list[150:200]]

    thread_num = 4
    threads = []
    for i in range(thread_num):
        threads.append(ThreadWithReturnValue(target=search_async, args=(q_split[i],)))
        threads[i].start()

    threads.append(ThreadWithReturnValue(target=load_json, args=(wiki_path,)))
    threads[4].start()

    # threads.append(ThreadWithReturnValue(target=load_json, args=(ques_path,)))
    # threads[5].start()

    for i in range(thread_num):
        threads[i].join()

    return threads[4].join(), json_q


def main():
    args = arg_parser_factory.build()
    start = time.time()

    # wiki_db 預處理
    if args.subcmd == 'pre':
        pre_process_wiki_db(wiki_path=args.input,
                            output_path=args.output)
    # 開始算分
    if args.subcmd == 'qa':
        wiki, ques = init_QA_bot(args.ques, args.input)
        print(start_QA_bot_input_json(wiki_db_json=wiki,
                                      question_json=ques))
    end = time.time()
    print('total time = ', end - start)


if __name__ == "__main__":
    main()
