import os

from Utils import Utils
from Error import Error
from defines import *
from Mail_sender import Mail_sender
from Logger import Logger


class Accounting_handler:

    def start(self):
        global users_download_volume
        users_download_volume = dict()

    def is_user_eligible_to_download(self, file_path, username):
        if Utils().is_accounting_enabled():
            return self.check_size_limit(file_path, username)

    def check_size_limit(self, file_path, username):
        if username not in users_download_volume:
            users_download_volume[username] = 0

        try:
            file_size = os.path.getsize(file_path)
        except Exception:
            raise Error(FILE_NOT_EXISTED)

        if users_download_volume[username] + file_size < int(Utils().get_user_download_limit(username)):
            self.alert_user_if_needed(int(Utils().get_user_download_limit(username)), username, file_size)
            users_download_volume[username] += file_size
            print(username, "download volume:", users_download_volume[username], "/",
                  Utils().get_user_download_limit(username))

            Logger.log(username + " download volume has changed: " + str(users_download_volume[username]) + "/" + str(
                Utils().get_user_download_limit(username)))
            return True
        else:
            print(username, "download volume:", users_download_volume[username], "/",
                  Utils().get_user_download_limit(username))
            print("file size:", file_size)
            print(users_download_volume[username] + file_size, " exceeds ", Utils().get_user_download_limit(username))
            Logger.log(username + " current download volume: " + str(users_download_volume[username]) + "/" + str(
                Utils().get_user_download_limit(username)))
            Logger.log(username + " can't download " + file_path + " because file size is " + str(file_size))
            raise Error(DOWNLOAD_LIMIT_EXCEEDED)

    def alert_user_if_needed(self, limit, username, file_size):
        if limit - users_download_volume[username] >= Utils().get_threshold():
            if limit - users_download_volume[username] - file_size <= Utils().get_threshold():
                email, alert = Utils().get_user_email_alert(username)
                if alert:
                    print("Alerting", username, "at", email)
                    Logger.log(
                        username + " is being alerted via email about going under remaining download volume threshold")
                    Mail_sender(email, THRESHOLD_SUBJECT, THRESHOLD_BODY).send()

    @staticmethod
    def can_access(username, file_path):
        authentication = Utils().get_authorization()
        enable = authentication["enable"]
        admins = authentication["admins"]
        files = authentication["files"]
        full_path_files = []
        for file in files:
            full_path_files.append(os.getcwd() + file[1:])

        if enable and username not in admins and file_path in full_path_files:
            Logger.log(username + " access blocked to " + file_path)
            raise Error(FILE_UNAVAILABLE)
            return False
        else:
            return True

    @staticmethod
    def remove_unauthorized_files(files_list, base_path, username):
        authorized_files = []
        for file in files_list:
            try:
                Accounting_handler.can_access(username, os.getcwd() + "/" + base_path + file)
                authorized_files.append(file)
            except Exception:
                pass
        return authorized_files