import json
from defines import *
from Error import Error

CONFIG_PATH = '../config.json'


class Utils:

    def read_config_file(self):
        global config_data
        config_file = open(CONFIG_PATH)
        config_data = json.load(config_file)

    def get_command_channel_port(self):
        return config_data["commandChannelPort"]

    def get_data_channel_port(self):
        return config_data["dataChannelPort"]
