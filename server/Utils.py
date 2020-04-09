import json
from defines import *
from Error import Error


class Utils:
    def get_diff_path(self, base_dir, curr_dir):
        base_dir_list = base_dir.split('/')
        curr_dir_list = curr_dir.split('/')
        result_dir_list = []
        for path in curr_dir_list:
            if path not in base_dir_list:
                result_dir_list.append(path)
        result_dir = '/'.join(result_dir_list)
        if result_dir:
            return result_dir + '/'
        return result_dir

    def read_config_file(self):
        global config_data
        config_file = open(CONFIG_PATH)
        config_data = json.load(config_file)

    def get_users(self):
        return config_data['users']

    def find_user(self, user_name):
        for user in self.get_users():
            if user['user'] == user_name:
                return user
        raise Error(INVALID_USERNAME_PASSWORD)

    def get_parsed_data(self, data):
        return list(map(str, data.split()))

    def get_command(self, data):
        try:
            return data[0]
        except:
            return ""

    def get_command_channel_port(self):
        return config_data["commandChannelPort"]

    def get_data_channel_port(self):
        return config_data["dataChannelPort"]

    def get_users_accounting(self):
        return config_data["accounting"]["users"]

    def find_user_by_username(self, users, username):
        for user in users:
            if user['user'] == username:
                return user
        raise Error(INVALID_USERNAME_PASSWORD)

    def get_user_download_limit(self, username):
        users = self.get_users_accounting()
        user = self.find_user_by_username(users, username)
        return user["size"]

    def is_accounting_enabled(self):
        return config_data["accounting"]["enable"]
