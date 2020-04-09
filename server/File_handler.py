import os
import pickle



class File_handler:
    def __init__(self):
        pass

    @staticmethod
    def get_directory_files_list(base_path):
        if not base_path:
            return os.listdir()
        else:
            return os.listdir(base_path)
