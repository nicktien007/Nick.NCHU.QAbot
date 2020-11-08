from utils import arg_parser_factory
from service.calc_score_service import start_QA_bot
from service.pre_process_service import pre_process_wiki_db


def main():
    args = arg_parser_factory.build()

    # wiki_db 預處理
    if args.subcmd == 'pre':
        pre_process_wiki_db(wiki_path=args.input,
                            output_path=args.output)
    # 開始算分
    if args.subcmd == 'qa':
        print(start_QA_bot(wiki_path=args.input,
                           question_path=args.ques))


if __name__ == "__main__":
    main()
