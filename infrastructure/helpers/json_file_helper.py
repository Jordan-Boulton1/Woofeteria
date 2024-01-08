import json


class JsonFileHelper:
    @staticmethod
    def read_from_config_file():
        config_file = open("./creds.json")
        data = json.load(config_file)
        return data