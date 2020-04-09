CONFIG_PATH = '../config.json'
IP = "127.0.0.1"

BAD_SEQUENCE_OF_COMMANDS = '503 Bad sequence of commands.'
INVALID_USERNAME_PASSWORD = '403 Invalid username or password.'
USERNAME_OK = '331 User name okey, need password.'
LOGIN_OK = '230 User logged in, proceed.'
NOT_AUTHORIZED = '332 Need account for login.'
MAX_SIZE = 1024
SYNTAX_ERROR = '501 Syntax error in parameters or arguments.'
FILE_EXISTED = '500 File or directory already existed in this path.'
FILE_NOT_EXISTED = '500 File or directory not existed in this path.'
NOT_DIRECTORY = '500 Not a directory.'
UNKNOWN_COMMAND = '500 Unknown command.'
LIST_TRANSFER_DONE = '226 List transfer done.'
CWD_SUCCESS = '250 Successful Change.'
QUIT_OK = '221 Successful Quit.'
SUCCESSFUL_DOWNLOAD = "‫‪226‬‬ ‫‪Successful‬‬ ‫‪Download.‬‬"
DOWNLOAD_LIMIT_EXCEEDED = "‫‪425‬‬ ‫‪Can't‬‬ ‫‪open‬‬ ‫‪data‬‬ ‫‪connection.‬‬"


HELP_TEXT = "214\n" + \
            "USER [name], Its argument is used to specify the user's string. It is used for user authentication.\n" + \
            "PASS [password], Its argument is used to specify the user's password. It is used for user authentication.\n" + \
            "PWD, It is used for printing current working directory\n" + \
            "MKD [flag] [name], Its argument is used to specify the file/directory path. Flag: -i, If present, a new file will be created and otherwise a new directory. It is usede for creating a new file or directory.\n" + \
            "RMD [flag] [name], Its argument is used to specify the file/directory path. Flag: -f, If present, a directory will be removed and otherwise a file. It is usede for removing a file or directory.\n" + \
            "LIST, It is used for printing list of file/directories exists in current working directory\n" + \
            "CWD [path], Its argument is used to specify the directory's path. It is used for changing the current working directory.\n" + \
            "DL [name], Its argument is used to specify the file's name. It is used for downloading a file.\n" + \
            "HELP, It is used for printing list of available commands.\n" + \
            "QUIT, It is used for signing out from the server.\n"