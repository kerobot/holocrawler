import os
import urllib.request
from dotenv import load_dotenv

class Settings:
    def __init__(self, envpath: str) -> None:
        """
        Settingsクラスのコンストラクタ

        :param envpath: .envファイルのパス
        """
        self.env_path: str = envpath
        self.__load_env()

        self.__holodule_url: str = self.__get_env("HOLODULE_URL")
        self.__api_key: str = self.__get_env("API_KEY")
        self.__api_service_name: str = self.__get_env("API_SERVICE_NAME")
        self.__api_version: str = self.__get_env("API_VERSION")
        self.__mongodb_user: str = self.__get_env("MONGODB_USER")
        self.__mongodb_password: str = self.__get_env("MONGODB_PASSWORD")
        self.__mongodb_host: str = self.__get_env("MONGODB_HOST")
        self.__youtube_url_pattern: str = self.__get_env("YOUTUBE_URL_PATTERN")

    @property
    def holodule_url(self) -> str:
        """
        ホロジュールのURLを取得する

        :return: ホロジュールのURL
        """
        return self.__holodule_url

    @property
    def api_key(self) -> str:
        """
        Youtube Data API v3 のAPIキーを取得する

        :return: APIキー
        """
        return self.__api_key

    @property
    def api_service_name(self) -> str:
        """
        Youtube Data API v3 のAPIサービス名を取得する

        :return: APIサービス名
        """
        return self.__api_service_name

    @property
    def api_version(self) -> str:
        """
        Youtube Data API v3 のAPIバージョンを取得する

        :return: APIバージョン
        """
        return self.__api_version

    @property
    def mongodb_user(self) -> str:
        """
        MongoDBのユーザーを取得する

        :return: MongoDBのユーザー
        """
        return self.__mongodb_user

    @property
    def mongodb_password(self) -> str:
        """
        MongoDBのパスワードを取得する

        :return: MongoDBのパスワード
        """
        return self.__mongodb_password

    @property
    def mongodb_host(self) -> str:
        """
        MongoDBのホスト:ポートを取得する

        :return: MongoDBのホスト:ポート
        """
        return self.__mongodb_host

    @property
    def youtube_url_pattern(self) -> str:
        """
        Youtube URL として判定するパターンを取得する

        :return: Youtube URL として判定するパターン
        """
        return self.__youtube_url_pattern

    def __load_env(self) -> None:
        """
        .envファイルを読み込む
        """
        try:
            load_dotenv(self.env_path)
        except Exception as e:
            raise ValueError(f"Failed to load .env file: {e}")

    def __get_env(self, key: str) -> str:
        """
        環境変数を取得する

        :param key: 環境変数のキー
        :return: 環境変数の値
        """
        value = os.environ.get(key)
        if value is None:
            raise ValueError(f"Missing environment variable: {key}")
        return value

    async def __check_url(self, url: str) -> bool:
        """
        指定したURLにアクセスできるかをチェックする

        :param url: チェックするURL
        :return: アクセスできる場合はTrue、できない場合はFalse
        """
        try:
            async with urllib.request.urlopen(url) as response:
                return True
        except Exception:
            return False

    async def check_holodule_url(self) -> bool:
        """
        ホロジュールのURLにアクセスできるかをチェックする

        :return: アクセスできる場合はTrue、できない場合はFalse
        """
        return await self.__check_url(self.__holodule_url)
