import csv
import pymongo
from typing import NoReturn, List
from app.holodule import Holodule
from logging import getLogger, DEBUG, NullHandler

class Holodules:
    def __init__(self, holodules: List = []):
        self._logger = getLogger(__name__)
        self._logger.addHandler(NullHandler())
        self._logger.setLevel(DEBUG)
        self._logger.propagate = True
        self.holodules = holodules
        self.index = 0

    def __iter__(self):
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

    def append(self, holodule: Holodule):
        self.holodules.append(holodule)

    def remove_at(self, index: int):
        self.holodules.pop(index)

    def output_to_csv(self, filepath: str):
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
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        try:
            video_ids = [holodule.video_id for holodule in self.holodules]
            collection.delete_many({"video_id": {"$in": video_ids}})
            docs = [holodule.to_dict() for holodule in self.holodules]
            collection.insert_many(docs)
        except pymongo.errors.PyMongoError as e:
            self._logger.error("MongoDB エラーが発生しました。%s", e, exc_info=True)
            raise
        finally:
            client.close()
