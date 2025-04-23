import json
import os
import pickle
from pathlib import Path


class PickleCache:
    @staticmethod
    def hash_fn(x) -> str:
        return json.dumps(x)

    # note: this method is NOT used.
    @classmethod
    def short_hash_fn(cls, x=None, hash=None):
        import hashlib

        if hash:
            assert x is None, "x and hash can not be truthy at the same time."

        hash = hash or cls.hash_fn(x)
        bytes = hash.encode("utf-8")
        return hashlib.sha256(bytes)

    def __init__(self, cache_file, cache_dir=".cache"):
        self.cache_path = os.path.join(cache_dir, cache_file)
        # print("cache_path is", self.cache_path)
        # print(os.getcwd())
        self.store = {}

    def load(self):
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "rb") as f:
                self.store = pickle.load(f)

    def save(self):
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(self.store, f)
        except FileNotFoundError:
            dir = Path(self.cache_path).parent
            dir.mkdir(parents=True, exist_ok=True)

            with open(self.cache_path, "wb") as f:
                pickle.dump(self.store, f)

    def __getitem__(self, key):
        return self.store[key]

    def get(self, key, default=None):
        return self.store.get(key, default)

    def __setitem__(self, key, value):
        self.store[key] = value
        self.save()

    def __delitem__(self, key):
        del self.store[key]
        self.save()

    def clear(self) -> None:
        self.store.clear()
        self.save()

    def __contains__(self, key):
        return key in self.store
