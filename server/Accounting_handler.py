import os

from Utils import Utils
from Error import Error
from defines import *
from Mail_sender import Mail_sender


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
            return True
        else:
            print(username, "download volume:", users_download_volume[username], "/",
                  Utils().get_user_download_limit(username))
            print("file size:", file_size)
            print(users_download_volume[username] + file_size, " exceeds ", Utils().get_user_download_limit(username))
            raise Error(DOWNLOAD_LIMIT_EXCEEDED)

    def alert_user_if_needed(self, limit, username, file_size):
        if limit - users_download_volume[username] >= Utils().get_threshold():
            if limit - users_download_volume[username] - file_size <= Utils().get_threshold():
                email, alert = Utils().get_user_email_alert(username)
                if alert:
                    print("Alerting", username, "at", email)
                    Mail_sender(email, THRESHOLD_SUBJECT, THRESHOLD_BODY).send()
