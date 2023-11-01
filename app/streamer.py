from typing import List, Dict

class Streamer:
    """
    Streamerクラスは、ホロライブの配信者を表すオブジェクトを作成するためのクラスです。
    """
    def __init__(self, code: str, name: str, group: str, affiliations: List[str], 
                 image_name: str, channel_id: str, is_retired: bool = False) -> None:
        """
        Streamerクラスのインスタンスを生成します。

        :param code: 配信者のコード
        :param name: 配信者の名前
        :param group: 配信者のグループ
        :param affiliations: 配信者の所属のリスト
        :param image_name: 配信者のプロフィール画像のファイル名
        :param channel_id: 配信者のYouTubeチャンネルID
        :param is_retired: 配信者が引退しているかどうか
        """
        self.__code: str = code
        self.__name: str = name
        self.__group: str = group
        self.__affiliations: List[str] = affiliations
        self.__image_name: str = image_name
        self.__channel_id: str = channel_id
        self.__is_retired: bool = is_retired

    @property
    def code(self) -> str:
        """
        配信者のコードを取得します。

        :return: 配信者のコード
        """
        return self.__code
    
    @property
    def name(self) -> str:
        """
        配信者の名前を取得します。

        :return: 配信者の名前
        """
        return self.__name
    
    @property
    def group(self) -> str:
        """
        配信者のグループを取得します。

        :return: 配信者のグループ
        """
        return self.__group
    
    @property
    def affiliations(self) -> List[str]:
        """
        配信者の所属のリストを取得します。

        :return: 配信者の所属のリスト
        """
        return self.__affiliations
    
    @property
    def image_name(self) -> str:
        """
        配信者のプロフィール画像のファイル名を取得します。

        :return: 配信者のプロフィール画像のファイル名
        """
        return self.__image_name
    
    @property
    def channel_id(self) -> str:
        """
        配信者のYouTubeチャンネルIDを取得します。

        :return: 配信者のYouTubeチャンネルID
        """
        return self.__channel_id
    
    @property
    def is_retired(self) -> bool:
        """
        配信者が引退しているかどうかを取得します。

        :return: 配信者が引退しているかどうか
        """
        return self.__is_retired

    def to_dict(self) -> Dict[str, str]:
        """
        Streamerオブジェクトを辞書形式に変換します。

        :return: Streamerオブジェクトの辞書形式
        """
        data: Dict[str, str] = {
            'code': str(self.code),
            'name': str(self.name),
            'group': str(self.group),
            'affiliations': str(self.affiliations),
            'image_name': str(self.image_name),
            'channel_id': str(self.channel_id),
            'is_retired': str(self.is_retired)
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Streamer':
        """
        辞書形式からStreamerオブジェクトに変換します。

        :param data: Streamerオブジェクトの辞書形式
        :return: Streamerオブジェクト
        """
        code = data['code']
        name = data['name']
        group = data['group']
        affiliations = eval(data['affiliations'])
        image_name = data['image_name']
        channel_id = data['channel_id']
        is_retired = eval(data['is_retired'])
        return cls(code, name, group, affiliations, image_name, channel_id, is_retired)
