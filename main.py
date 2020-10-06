import sys
import os
import argparse
from os.path import join, dirname
from app.settings import Settings
from app.holocrawler import HoloCrawler

RETURN_SUCCESS = 0
RETURN_FAILURE = -1

def main():
    # parser を作る（説明を指定できる）
    parser = argparse.ArgumentParser(description="ホロジュールのHTMLをSelenium + BeautifulSoup4 + Youtube API で解析して MongoDB へ登録")
    # コマンドライン引数を設定する（説明を指定できる）
    parser.add_argument("filepath", help="出力するCSVファイルのパス")
    # コマンドライン引数を解析する
    args = parser.parse_args()

    # ファイルパスの取得
    filepath = args.filepath
    # ディレクトリパスの取得と存在確認
    dirpath = os.path.dirname(filepath)
    print(f"出力ディレクトリパス : {dirpath}")
    if os.path.exists(dirpath) == False:
        print("エラー : 出力するCSVファイルのディレクトリパスが存在しません。")
        return RETURN_FAILURE

    try:
        # Settings インスタンス
        settings = Settings(join(dirname(__file__), '.env'))
        # HoloCrawler インスタンス
        holocrawler = HoloCrawler(settings)
        # ホロジュールの取得
        holodule_list = holocrawler.get_holodule_list()
        # ホロジュールの出力
        holocrawler.output_holodule_list(holodule_list, filepath)
        # ホロジュールの登録
        holocrawler.register_holodule_list(holodule_list)
        return RETURN_SUCCESS
    except:
        info = sys.exc_info()
        print(info[1])
        return RETURN_FAILURE

if __name__ == "__main__":
    sys.exit(main())
