import sys
import os
import argparse
from os.path import join, dirname
from app.settings import Settings
from app.holocrawler import HoloCrawler
from app.logger import get_logger

RETURN_SUCCESS = 0
RETURN_FAILURE = -1

# ロギングの設定
json_path = join(dirname(__file__), "config/logger.json")
log_dir = join(dirname(__file__), "log")
logger = get_logger(log_dir, json_path, False)

def main():
    # parser を作る（説明を指定できる）
    parser = argparse.ArgumentParser(description="ホロジュールのHTMLをSelenium + BeautifulSoup4 + Youtube API で解析して MongoDB へ登録")
    # コマンドライン引数を設定する（説明を指定できる）
    parser.add_argument("--csvpath", nargs="?", default="output.csv", help="出力するCSVファイルのパス（デフォルト: output.csv）")
    # コマンドライン引数を解析する
    args = parser.parse_args()

    # ファイルパスの取得
    is_output = False
    csvpath = args.csvpath
    if csvpath is not None:
        # ディレクトリパスの取得と存在確認
        dirpath = os.path.dirname(csvpath)
        logger.info("出力ディレクトリパス : %s", dirpath)
        if os.path.exists(dirpath) == False:
            logger.error("出力するCSVファイルのディレクトリパスが存在しません。 : %s", dirpath)
            return RETURN_FAILURE
        is_output = True

    try:
        # Settingsオブジェクト
        settings = Settings(join(dirname(__file__), '.env'))
        # HoloCrawlerオブジェクト
        holocrawler = HoloCrawler(settings)
        logger.info("ホロジュールの取得を開始します。")
        # ホロジュールの取得
        holodules = holocrawler.get_holodules()
        logger.info("ホロジュールを取得しました。 : %s件", len(holodules))
        # ホロジュールの登録
        holocrawler.save_to_mongodb()
        logger.info("ホロジュールを登録しました。")
        # ホロジュールの出力
        if is_output == True:
            holocrawler.output_to_csv(csvpath)
            logger.info("ホロジュールを出力しました。 : %s件", len(holodules))
        return RETURN_SUCCESS
    except:
        logger.error("エラーが発生しました。", exc_info=True)
        return RETURN_FAILURE

if __name__ == "__main__":
    sys.exit(main())
