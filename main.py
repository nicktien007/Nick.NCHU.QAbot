import time
from thirdparty.google import search_async
from utils import arg_parser_factory
from service.calc_score_service import start_QA_bot
from service.pre_process_service import pre_process_wiki_db


def main():
    args = arg_parser_factory.build()
    start = time.time()

    # wiki_db 預處理
    if args.subcmd == 'pre':
        pre_process_wiki_db(wiki_path=args.input,
                            output_path=args.output)
    # 開始算分
    if args.subcmd == 'qa':
        search_async(args.ques)
        print(start_QA_bot(wiki_path=args.input,
                           question_path=args.ques))

    end = time.time()
    print('total time = ', end - start)


if __name__ == "__main__":
    main()
