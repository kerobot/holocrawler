import os
import urllib.request
from dotenv import load_dotenv

class Settings:
    def __init__(self, envpath):
        # .env ファイルを明示的に指定して読み込む
        self.__dotenv_path = envpath
        load_dotenv(self.__dotenv_path)
        # ホロジュールのURL
        self.__holodule_url = os.environ.get("HOLODULE_URL")
        if self.check_url(self.__holodule_url) == False:
            raise ValueError("指定したURLにアクセスできません。")
        # Youtube Data API v3 の APIキー
        self.__api_key = os.environ.get("API_KEY")
        # Youtube Data API v3 の APIサービス名
        self.__api_service_name = os.environ.get("API_SERVICE_NAME")
        # Youtube Data API v3 の APIバージョン
        self.__api_version = os.environ.get("API_VERSION")
        # mongodb の ユーザー
        self.__mongodb_user = os.environ.get("MONGODB_USER")
        # mongodb の パスワード
        self.__mongodb_password = os.environ.get("MONGODB_PASSWORD")
        # mongodb の ホスト:ポート
        self.__mongodb_host = os.environ.get("MONGODB_HOST")

    @property
    def holodule_url(self):
        return self.__holodule_url

    @property
    def api_key(self):
        return self.__api_key

    @property
    def api_service_name(self):
        return self.__api_service_name

    @property
    def api_version(self):
        return self.__api_version

    @property
    def mongodb_user(self):
        return self.__mongodb_user

    @property
    def mongodb_password(self):
        return self.__mongodb_password

    @property
    def mongodb_host(self):
        return self.__mongodb_host

    def check_url(self, url):
        try:
            # 指定したURLにアクセスできるかをチェック
            with urllib.request.urlopen(url):
                return True
        except urllib.request.HTTPError:
            return False
