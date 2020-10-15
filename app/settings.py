import os
import urllib.request
from dotenv import load_dotenv

class Settings:
    def __init__(self, envpath):
        # .env ファイルを明示的に指定して環境変数として読み込む
        self.__dotenv_path = envpath
        load_dotenv(self.__dotenv_path)
        # 環境変数から設定値を取得
        self.__holodule_url = os.environ.get("HOLODULE_URL")
        if self.__check_url(self.__holodule_url) == False:
            raise ValueError("指定したURLにアクセスできません。")
        self.__api_key = os.environ.get("API_KEY")
        self.__api_service_name = os.environ.get("API_SERVICE_NAME")
        self.__api_version = os.environ.get("API_VERSION")
        self.__mongodb_user = os.environ.get("MONGODB_USER")
        self.__mongodb_password = os.environ.get("MONGODB_PASSWORD")
        self.__mongodb_host = os.environ.get("MONGODB_HOST")

    # ホロジュールのURL
    @property
    def holodule_url(self):
        return self.__holodule_url

    # Youtube Data API v3 の APIキー
    @property
    def api_key(self):
        return self.__api_key

    # Youtube Data API v3 の APIサービス名
    @property
    def api_service_name(self):
        return self.__api_service_name

    # Youtube Data API v3 の APIバージョン
    @property
    def api_version(self):
        return self.__api_version

    # mongodb の ユーザー
    @property
    def mongodb_user(self):
        return self.__mongodb_user

    # mongodb の パスワード
    @property
    def mongodb_password(self):
        return self.__mongodb_password

    # mongodb の ホスト:ポート
    @property
    def mongodb_host(self):
        return self.__mongodb_host

    # 指定したURLにアクセスできるかをチェック
    def __check_url(self, url):
        try:
            with urllib.request.urlopen(url):
                return True
        except urllib.request.HTTPError:
            return False
