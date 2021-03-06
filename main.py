import sys
import os
import argparse
from os.path import join, dirname
from app.settings import Settings
from app.holocrawler import HoloCrawler
from app.logger import log, get_logger

RETURN_SUCCESS = 0
RETURN_FAILURE = -1

# ロギングの設定
json_path = join(dirname(__file__), "config/logger.json")
log_dir = join(dirname(__file__), "log")
logger = get_logger(log_dir, json_path, False)

@log(logger)
def main():
    # parser を作る（説明を指定できる）
    parser = argparse.ArgumentParser(description="ホロジュールのHTMLをSelenium + BeautifulSoup4 + Youtube API で解析して MongoDB へ登録")
    # コマンドライン引数を設定する（説明を指定できる）
    parser.add_argument("--csvpath", help="出力するCSVファイルのパス（任意）")
    # コマンドライン引数を解析する
    args = parser.parse_args()

    # ファイルパスの取得
    is_output = False
    csvpath = args.csvpath
    if csvpath is not None:
        # ディレクトリパスの取得と存在確認
        dirpath = os.path.dirname(csvpath)
        logger.info(f"出力ディレクトリパス : {dirpath}")
        if os.path.exists(dirpath) == False:
            logger.error(f"出力するCSVファイルのディレクトリパスが存在しません。")
            return RETURN_FAILURE
        is_output = True

    try:
        # Settings インスタンス
        settings = Settings(join(dirname(__file__), '.env'))
        # HoloCrawler インスタンス
        holocrawler = HoloCrawler(settings)
        # ホロジュールの取得
        holodule_list = holocrawler.get_holodule_list()
        logger.info(f"ホロジュールを取得しました。 : {len(holodule_list)}件")
        # ホロジュールの登録
        holocrawler.register_holodule_list(holodule_list)
        logger.info(f"ホロジュールを登録しました。")
        # ホロジュールの出力
        if is_output == True:
            holocrawler.output_holodule_list(holodule_list, csvpath)
            logger.info(f"ホロジュールを出力しました。 : {len(holodule_list)}件")
        return RETURN_SUCCESS
    except:
        info = sys.exc_info()
        print(info[1])
        return RETURN_FAILURE

if __name__ == "__main__":
    sys.exit(main())
