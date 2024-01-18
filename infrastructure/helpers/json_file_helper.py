import json


class JsonFileHelper:
    """
    Helper class for reading from a JSON file.

    This class includes static methods for reading data from a JSON file.
    """
    @staticmethod
    def read_from_config_file():
        config_file = open("./creds.json")
        data = json.load(config_file)
        return data
