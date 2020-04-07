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
        return data[0]
