from datetime import datetime
import json


class DataCache:

    max_players: int
    online_players: int
    name: str
    motd: str
    favicon: str
    version: str
    active: bool
    last_image: str
    last_update: datetime

    def __init__(
        self,
        max_players=0,
        online_players=0,
        name=None,
        motd=None,
        favicon=None,
        version=None,
        active=False,
        last_image=None,
        last_update=None
    ):
        self.max_players = max_players
        self.online_players = online_players
        self.name = name
        self.motd = motd
        self.favicon = favicon
        self.version = version
        self.active = active
        self.last_image = last_image
        self.last_update = self.parse_datetime(last_update)

    def parse_datetime(self, obj):
        if not obj:
            return None
        if isinstance(obj, datetime):
            return obj
        else:
            return datetime.fromtimestamp(obj)

    def to_json(self):
        return json.dumps(self, default=self.json_default)

    def json_default(self, obj):
        if isinstance(obj, datetime):
            return obj.timestamp()
        else:
            return obj.__dict__


class Cacher:

    data: DataCache = DataCache()
    cache: str = None

    def __init__(self) -> None:
        self.read_cache()

    def has_changed(self):
        cache_dict: dict = json.loads(self.cache)
        data_dict: dict = json.loads(self.data.to_json())
        cache_dict.pop("last_image")
        data_dict.pop("last_image")
        return data_dict != cache_dict

    def create_cache(self):
        with open("cache.json", "w") as f:
            self.cache = self.data.to_json()
            f.write(self.cache)

    def write_cache(self):
        self.cache = self.data.to_json()
        with open("cache.json", "w") as f:
            f.write(self.cache)

    def read_cache(self):
        try:
            with open("cache.json", "r") as f:
                self.cache = f.read()

                # Check if the cache is valid
                json.loads(self.cache)
                if len(self.cache) == 0:
                    raise Exception("Cache is empty")

        # If the cache fails to load, create a new one
        except Exception as e:
            print(e)
            self.create_cache()

        # If the cache holds any invalid data,
        # or if cache key values have changed,
        # make sure to create a new cache to reflect these changes
        try:
            self.data = DataCache(**json.loads(self.cache))
        except TypeError:
            self.create_cache()
