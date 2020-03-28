""" It's quite often that I collect a large amount of files, around 100k.
    Many tools work much better if the number of files per directory is
    below ~100, For instance pycharm starts to work quite badly with more than
    1000 files per directory.
    This file provides tools to deal with this.
"""
from pathlib import Path
import hashlib
import json

LOCATION_KEY = "__location"


class FileCollection:
    def __init__(self, collection_path: Path):
        collection_path.mkdir(parents=True, exist_ok=True)
        self.collection_path = collection_path
        self.mapping = {}
        self.mapping_file = collection_path / "mapping.json"
        if self.mapping_file.exists():
            with open(self.mapping_file, "r") as f:
                self.mapping = json.loads(f.read())

    def has_filename(self, filename: str):
        return filename in self.mapping

    def add_metadata(self, filename: str, key: str, value: str):
        if filename not in self.mapping:
            self.get_disk_filepath(filename)
        self.mapping[filename][key] = value

    def get_metadata(self, filename: str, key: str):
        return self.mapping[filename].get(key)

    def get_disk_filepath(self, filename: str):
        """ Return the actual location on disk. Create the parent folder if needed.
        """
        hash = hashlib.md5(filename.encode("utf-8")).hexdigest()[0:2]
        file_location = self.collection_path / hash / filename
        if filename not in self.mapping:
            (self.collection_path / hash).mkdir(parents=True, exist_ok=True)
            file_location.parent.mkdir(parents=True, exist_ok=True)
            self.mapping[filename] = {LOCATION_KEY: str(Path(hash) / filename)}
        return str(file_location)

    def sync(self):
        with open(self.mapping_file, "w") as f:
            f.write(json.dumps(self.mapping, indent=2))
