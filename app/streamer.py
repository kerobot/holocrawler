class Streamer:
    def __init__(self, code: str, name: str, group: str, affiliations: list[str], 
                 image_name: str, channel_id: str, is_retired: bool = False):
        self.__code = code
        self.__name = name
        self.__group = group
        self.__affiliations = affiliations
        self.__image_name = image_name
        self.__channel_id = channel_id
        self.__is_retired = is_retired

    @property
    def code(self) -> str:
        return self.__code
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def group(self) -> str:
        return self.__group
    
    @property
    def affiliations(self) -> list[str]:
        return self.__affiliations
    
    @property
    def image_name(self) -> str:
        return self.__image_name
    
    @property
    def channel_id(self) -> str:
        return self.__channel_id
    
    @property
    def is_retired(self) -> bool:
        return self.__is_retired

    def to_dict(self) -> dict[str, str]:
        data = {
            'code': str(self.code),
            'name': str(self.name),
            'group': str(self.group),
            'affiliations': str(self.affiliations),
            'image_name': str(self.image_name),
            'channel_id': str(self.channel_id),
            'is_retired': str(self.is_retired)
        }
        return data
