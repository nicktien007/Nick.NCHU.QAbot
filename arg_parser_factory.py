from argparse import ArgumentParser, RawTextHelpFormatter


def build():
    parser = ArgumentParser(
        description='QA Bot 算分程式')

    subcmd = parser.add_subparsers(
        dest='subcmd', help='subcommands', metavar='SUBCOMMAND')
    subcmd.required = True

    # 資料預處理
    pre_parser = subcmd.add_parser('pre',
                                   help='wiki_db 預處理')
    pre_parser.add_argument('-i',
                            dest='input',
                            help='wiki_db檔案路徑')
    pre_parser.add_argument('-o',
                            dest='output',
                            help='輸出檔案路徑')

    # 進行QA算分
    qa_parser = subcmd.add_parser('qa',
                                  help='進行查詢')
    qa_parser.add_argument('-i',
                           dest='input',
                           help='wiki_db檔案路徑')
    qa_parser.add_argument('-q',
                           dest='ques',
                           help='QA問題檔案路徑')

    return parser.parse_args()
