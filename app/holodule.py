"""
ホロジュールの配信情報＋Youtubeの動画情報含む
"""

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
        "風真いろは" : "HL0605"
    }

    def __init__(self):
        self.__video_id = ""
        self.__datetime = None
        self.__name = ""
        self.__title = ""
        self.__url = ""
        self.__description = ""
        self.__published_at = ""
        self.__channel_id = ""
        self.__channel_title = ""
        self.__tags = []

    # キー
    @property
    def key(self):
        _code = self.code;
        _dttm = self.datetime.strftime("%Y%m%d_%H%M%S") if self.datetime is not None else ""
        return _code + "_" + _dttm if ( len(_code) > 0 and len(_dttm) > 0 ) else ""

    # コード
    @property
    def code(self):
        return Holodule.codes[self.name] if self.name in Holodule.codes else ""

    # video_id
    @property
    def video_id(self):
        return self.__video_id

    @video_id.setter
    def video_id(self, video_id):
        self.__video_id = video_id

    # 日時
    @property
    def datetime(self):
        return self.__datetime

    @datetime.setter
    def datetime(self, datetime):
        self.__datetime = datetime

    # 名前
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    # タイトル（Youtubeから取得）
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    # URL
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    # 説明（Youtubeから取得）
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    # 投稿日（Youtubeから取得）
    @property
    def published_at(self):
        return self.__published_at

    @published_at.setter
    def published_at(self, published_at):
        self.__published_at = published_at

    # チャンネルID（Youtubeから取得）
    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self.__channel_id = channel_id

    # チャンネルタイトル（Youtubeから取得）
    @property
    def channel_title(self):
        return self.__channel_title

    @channel_title.setter
    def channel_title(self, channel_title):
        self.__channel_title = channel_title

    # タグ（Youtubeから取得）
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        self.__tags = tags

    # ドキュメントへ変換
    def to_doc(self):
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
