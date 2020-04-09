from datetime import datetime

from Utils import Utils


class Logger:
    @staticmethod
    def log(msg):
        logging = Utils().get_logging()
        if logging["enable"]:
            with open(logging["path"], "a") as my_file:
                my_file.write(str(datetime.now()) + " -> " + msg + "\n")
