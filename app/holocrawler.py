"""
【ホロライブ】ホロジュールと Youtube の動画情報を取得して MongoDB へ登録する
"""

import re
import datetime
from logging import getLogger, DEBUG, NullHandler
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import quote_plus
from app.settings import Settings
from app.holodule import Holodule
from app.holodules import Holodules
from app.streamers import Streamers

class HoloCrawler:
    # コンストラクタ
    def __init__(self, settings: Settings):
        # Logger 関連
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True
        # WebDriver 関連
        self.__driver = None
        self.__wait = None
        # Model 関連
        self.__streamers = Streamers()
        self.__holodules = Holodules()
        # 設定情報の確認
        self._logger.debug('HOLODULE_URL : %s', settings.holodule_url)
        self._logger.debug('YOUTUBE_SETTING : %s, %s, %s', settings.api_service_name, settings.api_version, settings.api_key)
        self._logger.debug('MONGODB_SETTING : %s, %s, %s', settings.mongodb_user, settings.mongodb_password, settings.mongodb_host)
        self._logger.debug('YOUTUBE_PATTERN : %s', settings.youtube_url_pattern)
        # ホロジュールの URL
        self.__holodule_url = settings.holodule_url
        # YouTube Data API v3 を利用するための準備
        self.__youtube = build(settings.api_service_name, settings.api_version, developerKey=settings.api_key, cache_discovery=False)
        # mongodbのユーザー
        self.__mongodb_user = quote_plus(settings.mongodb_user)
        # mongodbのパスワード
        self.__mongodb_password = quote_plus(settings.mongodb_password)
        # mongodbの接続情報
        self.__mongodb_holoduledb = "mongodb://%s:%s@%s/holoduledb" % (self.__mongodb_user, self.__mongodb_password, settings.mongodb_host)
        self.__mongodb_db = "holoduledb"
        self.__mongodb_holodules = "holodules"
        self.__mongodb_streamers = "streamers"
        # youtube url の判定パターン
        self.__youtube_url_pattern = settings.youtube_url_pattern

    # ブラウザオプションの設定
    def __setup_options(self):
        options = webdriver.ChromeOptions()
        # ヘッドレスモードとする
        options.add_argument('--headless=new')
        return options

    # ホロジュールの取得
    def __get_holodules(self):
        # 取得対象の URL に遷移
        self.__driver.get(self.__holodule_url)
        # <div class="holodule" style="margin-top:10px;">が表示されるまで待機する
        self.__wait.until(EC.presence_of_element_located((By.CLASS_NAME, "holodule")))
        # ページソースの取得
        html = self.__driver.page_source.encode("utf-8")
        # ページソースの解析（パーサとして lxml を指定）
        soup = BeautifulSoup(html, "lxml")
        # タイトルの取得（確認用）
        head = soup.find("head")
        title = head.find("title").text
        self._logger.info('TITLE : %s', title)

        # TODO : ここからはページの構成に合わせて決め打ち = ページの構成が変わったら動かない
        # スケジュールの取得
        holodules = Holodules()
        date_string = ""
        today = datetime.date.today()
        tab_pane = soup.find("div", class_="tab-pane show active")
        containers = tab_pane.find_all("div", class_="container")

        for container in containers:
            # 日付のみ取得
            div_date = container.find("div", class_="holodule navbar-text")
            if div_date is not None:
                date_text = div_date.text.strip()
                match_date = re.search(r"[0-9]{1,2}/[0-9]{1,2}", date_text)
                dates = match_date.group(0).split("/")
                month = int(dates[0])
                day = int(dates[1])
                year = today.year
                if month == 12 and today.month == 1:
                    year = year - 1
                elif month == 1 and today.month == 12:
                    year = year + 1
                date_string = f"{year}/{month}/{day}"

            # ライバー毎のスケジュール
            thumbnails = container.find_all("a", class_="thumbnail")
            if thumbnails is not None:
                for thumbnail in thumbnails:
                    # Youtube URL
                    stream_url = thumbnail.get("href")
                    if stream_url is None or re.match(self.__youtube_url_pattern, stream_url) is None:
                        continue
                    # 時刻（先に取得しておいた日付と合体）
                    div_time = thumbnail.find("div", class_="col-4 col-sm-4 col-md-4 text-left datetime")
                    if div_time is None:
                        continue
                    time_text = div_time.text.strip()
                    match_time = re.search(r"[0-9]{1,2}:[0-9]{1,2}", time_text)
                    times = match_time.group(0).split(":")
                    hour = int(times[0])
                    minute = int(times[1])
                    datetime_string = f"{date_string} {hour}:{minute}"
                    stream_datetime = datetime.datetime.strptime(datetime_string, "%Y/%m/%d %H:%M")
                    # ライバーの名前
                    div_name = thumbnail.find("div", class_="col text-right name")
                    if div_name is None:
                        continue
                    stream_name = div_name.text.strip()
                    # リストに追加
                    streamer = self.__streamers.get_streamer_by_name(stream_name)
                    if streamer is None:
                        continue
                    holodule = Holodule(streamer.code, stream_url, stream_datetime, stream_name)
                    holodules.append(holodule)
        return holodules

    # Youtube 動画情報の取得
    def __get_youtube_video_info(self, youtube_url: str):
        try:
            self._logger.info('YOUTUBE_URL : %s', youtube_url)
            # Youtube の URL から ID を取得
            match_video = re.search(r"^[^v]+v=(.{11}).*", youtube_url)
            if not match_video:
                self._logger.error("YouTube URL が不正です。")
                return None
            video_id = match_video.group(1)

            # Youtube はスクレイピングを禁止しているので YouTube Data API (v3) で情報を取得
            search_response = self.__youtube.videos().list(
                # 結果として snippet のみを取得
                part="snippet",
                # 検索条件は id
                id=video_id,
                # 1件のみ取得
                maxResults=1
            ).execute()

            # 検索結果から情報を取得
            for search_result in search_response.get("items", []):
                # id
                video_id = search_result["id"]
                # タイトル
                title = search_result["snippet"]["title"]
                # 説明
                description = search_result["snippet"]["description"]
                # 投稿日
                published_at = search_result["snippet"]["publishedAt"]
                # チャンネルID
                channel_id = search_result["snippet"]["channelId"]
                # チャンネルタイトル
                channel_title = search_result["snippet"]["channelTitle"]
                # タグ（設定されていない＝キーが存在しない場合あり）
                tags = search_result["snippet"].setdefault("tags", [])
                # 取得した情報を返却
                return (video_id, title, description, published_at, channel_id, channel_title, tags)

            self._logger.error("指定したIDに一致する動画がありません。")
            return None

        except HttpError as e:
            self._logger.error("HTTP エラー %d が発生しました。%s" % (e.resp.status, e.content))
            raise
        except Exception as e:
            self._logger.error("エラーが発生しました。%s" % e)
            raise

    # ホロジュールのスクレイピングと Youtube 動画情報から、配信情報リストの取得
    def get_holodules(self):
        try:
            # オプションのセットアップ
            options = self.__setup_options()
            # ドライバの初期化（オプション（ヘッドレスモード）とプロファイルを指定）
            self.__driver = webdriver.Chrome(options=options)
            # 指定したドライバに対して最大で10秒間待つように設定する
            self.__wait = WebDriverWait(self.__driver, 10)
            # ホロジュールの取得
            self.__holodules = self.__get_holodules()
            # Youtube情報の取得
            for holodule in self.__holodules:
                try:
                    self._logger.info('HOLODULE_NAME : %s', holodule.name)
                    self._logger.info('HOLODULE_DATETIME : %s', holodule.datetime)
                    video_info = self.__get_youtube_video_info(holodule.url)
                    if video_info == None:
                        continue
                    holodule.set_video_info(*video_info)
                    self._logger.info('VIDEO_TITLE : %s', holodule.title)
                except Exception as e:
                    self._logger.error("エラーが発生しました。", exc_info=True)
                    raise e
        except Exception as e:
            self._logger.error("エラーが発生しました。", exc_info=True)
            raise e
        finally:
            # ドライバを閉じる
            if self.__driver is not None and len(self.__driver.window_handles) > 0:
                self.__driver.close()
        return self.__holodules

    # MongoDB への登録
    def save_to_mongodb(self):
        # ストリーマ情報の登録
        self.__streamers.save_to_mongodb(self.__mongodb_holoduledb, self.__mongodb_db, self.__mongodb_streamers)
        # ホロジュール情報の登録
        self.__holodules.save_to_mongodb(self.__mongodb_holoduledb, self.__mongodb_db, self.__mongodb_holodules)

    # CSV への出力
    def output_to_csv(self, filepath: str):
        # ホロジュール情報の出力
        self.__holodules.output_to_csv(filepath)
