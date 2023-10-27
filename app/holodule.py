import re
import datetime
from typing import List

class Holodule:
    def __init__(self, code: str = "", url: str = "", datetime: datetime = None, name: str = ""):
        self.__code = code
        self.__url = url
        self.__datetime = datetime
        self.__name = name
        self.__video_id = ""
        self.__title = ""
        self.__description = ""
        self.__published_at = ""
        self.__channel_id = ""
        self.__channel_title = ""
        self.__tags = []

    @property
    def key(self) -> str:
        _code = self.__code;
        _dttm = self.__datetime.strftime("%Y%m%d_%H%M%S") if self.__datetime is not None else ""
        return _code + "_" + _dttm if ( len(_code) > 0 and len(_dttm) > 0 ) else ""

    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def url(self) -> str:
        return self.__url
    
    @property
    def datetime(self) -> datetime:
        return self.__datetime
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def video_id(self) -> str:
        return self.__video_id
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def published_at(self) -> str:
        return self.__published_at
    
    @property
    def channel_id(self) -> str:
        return self.__channel_id
    
    @property
    def channel_title(self) -> str:
        return self.__channel_title
    
    @property
    def tags(self) -> List[str]:
        return self.__tags

    def set_video_info(self, video_id: str, title: str, description: str, published_at: str, channel_id: str, channel_title: str, tags: List[str]):
        self.__video_id = video_id
        self.__title = title
        self.__description = re.sub(r'[\r\n\"\']', '', description)[:1000]
        self.__published_at = published_at
        self.__channel_id = channel_id
        self.__channel_title = channel_title
        self.__tags = tags

    def to_dict(self) -> dict[str, str]:
        data = {
            'key': str(self.key),
            'code': str(self.code),
            'video_id': str(self.video_id),
            'datetime': str(self.datetime.strftime("%Y%m%d %H%M%S")),
            'name': str(self.name),
            'title': str(self.title),
            'url': str(self.url),
            'description': str(self.description),
            'published_at': str(self.published_at),
            'channel_id': str(self.channel_id),
            'channel_title': str(self.channel_title),
            'tags': str(self.tags)
        }
        return data
