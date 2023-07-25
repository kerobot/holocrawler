"""
【ホロライブ】ホロジュールと Youtube の動画情報を取得して MongoDB へ登録する
"""

import sys
import os
import csv
import re
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apiclient.discovery import build
from apiclient.errors import HttpError
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson.objectid import ObjectId
from app.settings import Settings
from app.holodule import Holodule

CHROMEDRIVER = "/usr/bin/chromedriver"
if os.name == "nt":
    CHROMEDRIVER = ".\chromedriver.exe"

class HoloCrawler:
    def __init__(self, settings):
        self.__driver = None
        self.__wait = None
        # ホロジュールの URL
        self.__holodule_url = settings.holodule_url
        # YouTube Data API v3 を利用するための準備
        self.__youtube = build(settings.api_service_name, settings.api_version, developerKey=settings.api_key, cache_discovery=False)
        # mongodbのユーザー
        self.__mongodb_user = quote_plus(settings.mongodb_user)
        # mongodbのパスワード
        self.__mongodb_password = quote_plus(settings.mongodb_password)
        # mongodbの接続情報
        self.__mongodb_host = "mongodb://%s/" % (settings.mongodb_host)
        # youtube url の判定パターン
        self.__youtube_url_pattern = settings.youtube_url_pattern

    # Firefoxオプションの設定
    def __setup_options(self):
        options = Options()
        # ヘッドレスモードとする
        options.add_argument("--headless")
        return options

    # ホロジュールの取得
    def __get_holodule(self):
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
        print(title)
        # TODO : ここからはページの構成に合わせて決め打ち = ページの構成が変わったら動かない
        # スケジュールの取得
        holodule_list = []
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
                # print(date_string)
            # ライバー毎のスケジュール
            thumbnails = container.find_all("a", class_="thumbnail")
            if thumbnails is not None:
                for thumbnail in thumbnails:
                    holodule = Holodule()
                    # Youtube URL
                    youtube_url = thumbnail.get("href")
                    if youtube_url is None or re.match(self.__youtube_url_pattern, youtube_url) is None:
                        continue
                    else:
                        holodule.url = youtube_url
                        # print(holodule.url)
                    # 時刻（先に取得しておいた日付と合体）
                    div_time = thumbnail.find("div", class_="col-4 col-sm-4 col-md-4 text-left datetime")
                    if div_time is None:
                        continue
                    else:
                        time_text = div_time.text.strip()
                        match_time = re.search(r"[0-9]{1,2}:[0-9]{1,2}", time_text)
                        times = match_time.group(0).split(":")
                        hour = int(times[0])
                        minute = int(times[1])
                        datetime_string = f"{date_string} {hour}:{minute}"
                        holodule.datetime = datetime.datetime.strptime(datetime_string, "%Y/%m/%d %H:%M")
                        # print(holodule.datetime)
                    # ライバーの名前
                    div_name = thumbnail.find("div", class_="col text-right name")
                    if div_name is None:
                        continue
                    else:
                        holodule.name = div_name.text.strip()
                        # print(holodule.name)
                    # リストに追加
                    if len(holodule.key) > 0:
                        holodule_list.append(holodule)
        return holodule_list

    # Youtube 動画情報の取得
    def __get_youtube_video_info(self, youtube_url):
        try:
            # Youtube の URL から ID を取得
            match_video = re.search(r"^[^v]+v=(.{11}).*", youtube_url)
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
                vid = search_result["id"]
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
                return (vid, title, description, published_at, channel_id, channel_title, tags)
            return ("","","","","","",[])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print(youtube_url)
            raise

    # ホロジュールのスクレイピングと Youtube 動画情報から、配信情報リストの取得
    def get_holodule_list(self):
        try:
            # オプションのセットアップ
            options = self.__setup_options()
            # ドライバの初期化（オプション（ヘッドレスモード）とプロファイルを指定）
            self.__driver = webdriver.Chrome(CHROMEDRIVER, options=options)
            # 指定したドライバに対して最大で10秒間待つように設定する
            self.__wait = WebDriverWait(self.__driver, 10)
            # ホロジュールの取得
            holodule_list = self.__get_holodule()
            # Youtube情報の取得
            for holodule in holodule_list:
                try:
                    # video情報
                    video_info = self.__get_youtube_video_info(holodule.url)
                    # video_id
                    holodule.video_id = video_info[0]
                    # タイトル
                    holodule.title = video_info[1]
                    # 説明文（長いので1000文字で切っている）
                    holodule.description = video_info[2].replace("\r","").replace("\n","").replace("\"","").replace("\'","")[:1000]
                    # 投稿日
                    holodule.published_at = video_info[3]
                    # チャンネルID
                    holodule.channel_id = video_info[4]
                    # チャンネルタイトル
                    holodule.channel_title = video_info[5]
                    # タグ
                    holodule.tags = video_info[6]
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise
            # 生成したリストを返す
            return holodule_list
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            # ドライバを閉じる
            self.__driver.close()

    # 配信情報リストのCSV出力
    def output_holodule_list(self, holodule_list, filepath):
        try:
            # CSV出力(BOM付きUTF-8)
            with open(filepath, "w", newline="", encoding="utf_8_sig") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow(["key","code", "video_id", "datetime", "name", "title", "url", "description", "published_at", "channel_id", "channel_title", "tags"])
                for holodule in holodule_list:
                    csvwriter.writerow([holodule.key, 
                                        holodule.code, 
                                        holodule.video_id, 
                                        holodule.datetime, 
                                        holodule.name, 
                                        holodule.title, 
                                        holodule.url, 
                                        holodule.description,
                                        holodule.published_at,
                                        holodule.channel_id,
                                        holodule.channel_title,
                                        holodule.tags])
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            pass

    # 配信情報リストのDB登録
    def register_holodule_list(self, holodule_list):
        try:
            # MongoDB のコレクションからの削除と挿入
            client = MongoClient(self.__mongodb_host)
            db = client.holoduledb
            db.authenticate(name=self.__mongodb_user,password=self.__mongodb_password)
            collection = db.holodules
            for holodule in holodule_list:
                # video_id を条件としたドキュメントの削除
                video_id = holodule.video_id
                collection.delete_one( {"video_id":video_id} )
                # ドキュメントの挿入
                doc = holodule.to_doc()
                collection.insert_one(doc)
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            pass
