from pymongo import MongoClient
import os

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseSingleton(metaclass=SingletonMeta):
    _db = None

    def __init__(self) -> None:
        self._db = MongoClient(host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")), username=os.getenv("DB_USERNAME"), password=os.getenv("DB_PASSWORD"))

    def get_db_connection(self):
        return self._db