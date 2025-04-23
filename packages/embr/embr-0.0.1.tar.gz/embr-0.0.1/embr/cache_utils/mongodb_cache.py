import os
from dataclasses import asdict
from textwrap import dedent
import json

from pymongo import MongoClient


DEFAULT_URI = os.environ.get("THREADS_MONGODB_URI")
DEFAULT_USERNAME = os.environ.get("THREADS_MONGODB_USERNAME")
DEFAULT_PASSWORD = os.environ.get("THREADS_MONGODB_PASSWORD")
DEFAULT_DB = os.environ.get("THREADS_MONGODB_CACHE_DB", "embr_cache")


def to_dict(o):
    if hasattr(o, "__dataclass_fields__"):
        data = asdict(o)
    elif isinstance(o, (list, tuple)):
        data = tuple([to_dict(v) for v in o])
    elif isinstance(o, (str, int, float, bool)):
        data = o
    elif isinstance(o, dict):
        data = {k: to_dict(v) for k, v in o.items()}
    else:
        raise TypeError("Type is not supported")

    return data


class MongoDBCache:
    @staticmethod
    def hash_fn(o):
        d = to_dict(o)
        return json.dumps(d)

    # @staticmethod
    # def get_doc_id(hash):
    #     pass

    def __init__(self, collection, db_name=None, uri=None, username=None, password=None):
        self.uri = uri or DEFAULT_URI
        self.username = username or DEFAULT_USERNAME
        self.password = password or DEFAULT_PASSWORD

        # print(db_name)

        self.db_name = db_name or DEFAULT_DB
        self.collection_name = collection or "cache"

        self.store = {}

        # self.load()

    def __repr__(self):
        return dedent(f"""
        ========================================
                    MongoDBCache
        ----------------------------------------
                     uri: {self.uri}
               username: {self.username}
                db_name: {self.db_name}
        collection_name: {self.collection_name}
        ----------------------------------------
        """)

    def load(self):
        self.client = MongoClient(
            self.uri,
            username=self.username,
            password=self.password,
            # authSource="lucidsim",
            # authMechanism="SCRAM-SHA-256",
        )

        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def save(self):
        pass

    def __getitem__(self, key):
        doc = self.collection.find_one({"key": key})
        if doc:
            return doc.get("value", None)

        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key, value):
        # _prefix = value.pop("_prefix", None)
        doc_id = self.collection.insert_one(
            {
                "key": key,
                "value": value,
                # "prefix": None,
            }
        ).inserted_id
        # Ge: this is perfect.
        return doc_id

    def __delitem__(self, key):
        self.collection.delete_one({"key": key})

    def clear(self) -> None:
        self.collection.deleteMany({})

    def __contains__(self, key):
        doc = self.collection.find_one({"key": key})
        if doc:
            return True
        else:
            return False
