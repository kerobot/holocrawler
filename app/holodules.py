import csv
import pymongo
from typing import NoReturn, List
from app.holodule import Holodule
from logging import getLogger, DEBUG, NullHandler

class Holodules:
    """
    Holodule オブジェクトのリストを管理するクラス。

    Attributes
    ----------
    holodules : List
        Holodule オブジェクトのリスト。
    index : int
        イテレータの現在位置を示すインデックス。

    Methods
    -------
    __iter__() -> Holodules
        イテレータを初期化する。
    __next__() -> Holodule
        次の Holodule オブジェクトを返す。
    __len__() -> int
        Holodule オブジェクトの数を返す。
    __getitem__(index: int) -> Holodule
        指定されたインデックスの Holodule オブジェクトを返す。
    append(holodule: Holodule) -> None
        Holodule オブジェクトをリストに追加する。
    remove_at(index: int) -> None
        指定されたインデックスの Holodule オブジェクトをリストから削除する。
    output_to_csv(filepath: str) -> None
        Holodule オブジェクトのリストを CSV ファイルに出力する。
    save_to_mongodb(uri: str, db_name: str, collection_name: str) -> NoReturn
        Holodule オブジェクトのリストを MongoDB に保存する。
    """
    def __init__(self, holodules: List[Holodule] = []) -> None:
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True
        self.holodules: List[Holodule] = holodules
        self.index: int = 0

    def __iter__(self) -> 'Holodules':
        self.index = 0
        return self

    def __next__(self) -> Holodule:
        if self.index < len(self.holodules):
            result = self.holodules[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def __len__(self) -> int:
        return len(self.holodules)

    def __getitem__(self, index: int) -> Holodule:
        return self.holodules[index]

    def append(self, holodule: Holodule) -> None:
        """
        Holodule オブジェクトをリストに追加する。

        Parameters
        ----------
        holodule : Holodule
            追加する Holodule オブジェクト。
        """
        self.holodules.append(holodule)

    def remove_at(self, index: int) -> None:
        """
        指定されたインデックスの Holodule オブジェクトをリストから削除する。

        Parameters
        ----------
        index : int
            削除する Holodule オブジェクトのインデックス。
        """
        self.holodules.pop(index)

    def output_to_csv(self, filepath: str) -> None:
        """
        Holodule オブジェクトのリストを CSV ファイルに出力する。

        Parameters
        ----------
        filepath : str
            出力する CSV ファイルのパス。
        """
        try:
            with open(filepath, "w", newline="", encoding="utf_8_sig") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow([attr for attr in vars(Holodule())])
                for holodule in self.holodules:
                    csvwriter.writerow([value for value in vars(holodule).values()])
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error("CSV エラーが発生しました。%s", e, exc_info=True)
            raise

    def save_to_mongodb(self, uri: str, db_name: str, collection_name: str) -> NoReturn:
        """
        Holodule オブジェクトのリストを MongoDB に保存する。

        Parameters
        ----------
        uri : str
            MongoDB の URI。
        db_name : str
            データベース名。
        collection_name : str
            コレクション名。
        """
        try:
            client = pymongo.MongoClient(uri)
            db = client[db_name]
            collection = db[collection_name]
            video_ids = [holodule.video_id for holodule in self.holodules]
            collection.delete_many({"video_id": {"$in": video_ids}})
            docs = [holodule.to_dict() for holodule in self.holodules]
            collection.insert_many(docs)
        except pymongo.errors.ConnectionError as e:
            self._logger.error("MongoDB 接続に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.OperationFailure as e:
            self._logger.error("MongoDB 操作に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.PyMongoError as e:
            self._logger.error("MongoDB エラーが発生しました。%s", e, exc_info=True)
            raise
        finally:
            client.close()
