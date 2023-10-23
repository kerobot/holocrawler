"""
ホロジュールの配信情報＋Youtubeの動画情報含む
"""

import datetime
from typing import List, NoReturn

class Holodule:
    codes = {
        "ホロライブ" : "HL0000",
        "ときのそら"  : "HL0001",
        "ロボ子さん" : "HL0002",
        "さくらみこ" : "HL0003",
        "星街すいせい" : "HL0004",
        "AZKi" : "HL0005",
        "夜空メル" : "HL0101",
        "アキ・ローゼンタール" : "HL0102",
        "赤井はあと" : "HL0103",
        "白上フブキ" : "HL0104",
        "夏色まつり" : "HL0105",
        "湊あくあ" : "HL0201",
        "紫咲シオン" : "HL0202",
        "百鬼あやめ" : "HL0203",
        "癒月ちょこ" : "HL0204",
        "大空スバル" : "HL0205",
        "大神ミオ" : "HL0G02",
        "猫又おかゆ" : "HL0G03",
        "戌神ころね" : "HL0G04",
        "兎田ぺこら" : "HL0301",
        "潤羽るしあ" : "HL0302",
        "不知火フレア" : "HL0303",
        "白銀ノエル" : "HL0304",
        "宝鐘マリン" : "HL0305",
        "天音かなた" : "HL0401",
        "桐生ココ" : "HL0402",
        "角巻わため" : "HL0403",
        "常闇トワ" : "HL0404",
        "姫森ルーナ" : "HL0405",
        "獅白ぼたん" : "HL0501",
        "雪花ラミィ" : "HL0502",
        "尾丸ポルカ" : "HL0503",
        "桃鈴ねね" : "HL0504",
        "魔乃アロエ" : "HL0505",
        "ラプラス" : "HL0601",
        "鷹嶺ルイ" : "HL0602",
        "博衣こより" : "HL0603",
        "沙花叉クロヱ" : "HL0604",
        "風真いろは" : "HL0605",
        "hololive DEV_IS" : "HLDI00",
        "火威青" : "HLDI01",
        "儒烏風亭らでん" : "HLDI02",
        "一条莉々華" : "HLDI03",
        "音乃瀬奏" : "HLDI04",
        "轟はじめ" : "HLDI05",
        "Risu" : "HLID01",
        "Moona" : "HLID02",
        "Iofi" : "HLID03",
        "Ollie" : "HLID04",
        "Anya" : "HLID05",
        "Reine" : "HLID06",
        "Zeta" : "HLID07",
        "Kaela" : "HLID08",
        "Kobo" : "HLID09",
        "Calli" : "HLEN01",
        "Kiara" : "HLEN02",
        "Ina" : "HLEN03",
        "Gura" : "HLEN04",
        "Amelia" : "HLEN05",
        "IRyS" : "HLEN06",
        "Fauna" : "HLEN07",
        "Kronii" : "HLEN08",
        "Mumei" : "HLEN09",
        "Baelz" : "HLEN10",
        "Shiori" : "HLEN11",
        "Bijou" : "HLEN12",
        "Nerissa" : "HLEN13",
        "FUWAMOCO" : "HLEN14",
        "Fuwawa" : "HLEN15",
        "Mococo" : "HLEN16",
        "Sana" : "HLEN17"
    }

    # コンストラクタ
    def __init__(self, video_id: str = "", datetime: datetime = None, name: str = "", title: str = "", url: str = "", description: str = "", published_at: str = "", channel_id: str = "", channel_title: str = "", tags: List[str] = []):
        self.__video_id = video_id
        self.__datetime = datetime
        self.__name = name
        self.__title = title
        self.__url = url
        self.__description = description
        self.__published_at = published_at
        self.__channel_id = channel_id
        self.__channel_title = channel_title
        self.__tags = tags

    # キー
    @property
    def key(self) -> str:
        _code = self.code;
        _dttm = self.datetime.strftime("%Y%m%d_%H%M%S") if self.datetime is not None else ""
        return _code + "_" + _dttm if ( len(_code) > 0 and len(_dttm) > 0 ) else ""

    # コード
    @property
    def code(self) -> str:
        return Holodule.codes[self.name] if self.name in Holodule.codes else ""

    # video_id
    @property
    def video_id(self) -> str:
        return self.__video_id

    @video_id.setter
    def video_id(self, video_id: str) -> NoReturn:
        self.__video_id = video_id

    # 日時
    @property
    def datetime(self) -> datetime:
        return self.__datetime

    @datetime.setter
    def datetime(self, datetime: datetime) -> NoReturn:
        self.__datetime = datetime

    # 名前
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> NoReturn:
        self.__name = name

    # タイトル（Youtubeから取得）
    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> NoReturn:
        self.__title = title

    # URL
    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str) -> NoReturn:
        self.__url = url

    # 説明（Youtubeから取得）
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str) -> NoReturn:
        self.__description = description

    # 投稿日（Youtubeから取得）
    @property
    def published_at(self) -> str:
        return self.__published_at

    @published_at.setter
    def published_at(self, published_at: str) -> NoReturn:
        self.__published_at = published_at

    # チャンネルID（Youtubeから取得）
    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id: str) -> NoReturn:
        self.__channel_id = channel_id

    # チャンネルタイトル（Youtubeから取得）
    @property
    def channel_title(self) -> str:
        return self.__channel_title

    @channel_title.setter
    def channel_title(self, channel_title: str) -> NoReturn:
        self.__channel_title = channel_title

    # タグ（Youtubeから取得）
    @property
    def tags(self) -> str:
        return self.__tags

    @tags.setter
    def tags(self, tags: str) -> NoReturn:
        self.__tags = tags

    # ドキュメントへ変換
    def to_doc(self) -> dict[str, str]:
        doc = { 'key': str(self.key),
                'code' : str(self.code),
                'video_id': str(self.video_id),
                'datetime' : str(self.datetime.strftime("%Y%m%d %H%M%S")),
                'name' : str(self.name),
                'title' : str(self.title),
                'url' : str(self.url),
                'description' : str(self.description),
                'published_at' : str(self.published_at),
                'channel_id' : str(self.channel_id),
                'channel_title' : str(self.channel_title),
                'tags' : str(self.tags)}
        return doc
