import json
from pathlib import Path


class DataParser:
    def __init__(self):
        self.test_data_path = Path(__file__).resolve().parent.parent / "testdata"

    async def get_index_data_from_file(self, file_name: str):
        with open(self.test_data_path / file_name, "r") as index_settings_file:
            index_settings = json.load(index_settings_file)
            return index_settings["settings"], index_settings["mappings"]

    async def get_data_from_file(self, file_name: str):
        with open(self.test_data_path / file_name, "r") as file_data:
            file_data = json.load(file_data)
            return file_data
