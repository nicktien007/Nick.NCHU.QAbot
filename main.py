from calc_score_service import start_QA_bot
from pre_process_service import pre_process_wiki_db


def main():
    # wiki_db 預處理
    # pre_process_wiki_db(wiki_path="./dataset/wiki_db_art_final_v1.txt",
    #                     output_path="./dataset/wiki_db_art_final_v2_j.json")

    # 開始算分
    print(start_QA_bot(wiki_path="./dataset/wiki_db_art_final_v2_j.json",
                       question_path="./dataset/question.json"))


if __name__ == "__main__":
    main()
